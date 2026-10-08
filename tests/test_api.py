"""REQ-API-001: local evaluation API."""

import json

import pytest
from fastapi import APIRouter, Depends, FastAPI
from starlette.testclient import TestClient

from decision_engine.api import create_app
from decision_engine.api.guards import (
    CONTENT_SECURITY_POLICY,
    MAX_BODY_BYTES,
    BodyLimitMiddleware,
    SecurityHeadersMiddleware,
    is_loopback,
    require_local_client,
)
from decision_engine.core import RuleRegistry, RuleSet

from .conftest import BASELINE, facts_payload, make_policy, rule_data, split_evenly

LOCAL = ("127.0.0.1", 50000)
SSN_LIKE_VALUE = "123-45-6789"


@pytest.fixture
def app():
    registry = RuleRegistry([RuleSet(data=rule_data(), logic=split_evenly)])
    policies = {"baseline": BASELINE, "test-bank": make_policy(additional_waiting_days=5)}
    return create_app(rules=registry, policies=policies)


@pytest.fixture
def client(app):
    return TestClient(app, client=LOCAL)


def _evaluate(client, payload=None, **overrides):
    body = (
        payload
        if payload is not None
        else {"policy": "baseline", "facts": facts_payload(), **overrides}
    )
    return client.post(
        "/v1/evaluate", content=json.dumps(body), headers={"content-type": "application/json"}
    )


def test_evaluate_returns_decision_envelope(client):
    response = _evaluate(client)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"]["outcome"] == "determined"
    assert body["decision"]["policy"]["institution"] == "baseline"
    assert len(body["facts_hash"]) == 64
    assert body["engine_version"]


def test_policy_choice_is_applied(client):
    base = _evaluate(client).json()["decision"]["determination"]["release_date"]
    stricter = _evaluate(client, policy="test-bank").json()["decision"]["determination"][
        "release_date"
    ]
    assert stricter["policy_days_added"] == 5
    assert base["policy_days_added"] == 0


def test_facts_hash_is_stable_for_equal_facts(client):
    assert _evaluate(client).json()["facts_hash"] == _evaluate(client).json()["facts_hash"]


def test_invalid_facts_report_paths_not_values(client):
    facts = facts_payload(ssn=SSN_LIKE_VALUE)
    response = _evaluate(client, {"policy": "baseline", "facts": facts})
    assert response.status_code == 422
    assert SSN_LIKE_VALUE not in response.text
    assert {"loc": ["facts", "ssn"], "type": "extra_forbidden"} in response.json()["errors"]


@pytest.mark.parametrize("raw", [b"{not json", b"[]", b'{"facts": {}}'])
def test_malformed_requests_are_rejected(client, raw):
    response = client.post(
        "/v1/evaluate", content=raw, headers={"content-type": "application/json"}
    )
    assert response.status_code == 422


def test_unknown_policy_is_404(client):
    response = _evaluate(client, policy="other-bank")
    assert response.status_code == 404
    assert response.json() == {"detail": "unknown_policy"}


def test_policy_must_be_an_id_not_a_path(client):
    response = _evaluate(client, policy="../../etc/passwd")
    assert response.status_code == 422


def test_meta_lists_versions_and_policies(client):
    meta = client.get("/v1/meta").json()
    assert meta["facts_schema_version"] == "4"
    assert meta["decision_schema_version"] == "2"
    assert [p["id"] for p in meta["policies"]] == ["baseline", "test-bank"]
    assert len(meta["registry_hash"]) == 64


@pytest.mark.parametrize("path", ["/v1/meta", "/v1/evaluate", "/", "/anything"])
def test_non_loopback_clients_are_refused_everywhere(app, path):
    remote = TestClient(app, client=("203.0.113.9", 50000))
    response = remote.post(path) if path == "/v1/evaluate" else remote.get(path)
    assert response.status_code == 403


def test_require_local_client_rejects_remote_scope():
    bare = FastAPI()
    router = APIRouter(dependencies=[Depends(require_local_client)])

    @router.get("/x")
    def x():
        return {"ok": True}

    bare.include_router(router)
    assert TestClient(bare, client=("203.0.113.9", 1)).get("/x").status_code == 403
    assert TestClient(bare, client=LOCAL).get("/x").status_code == 200


def test_oversized_bodies_are_rejected_before_parsing(client):
    big = b"{" + b" " * (MAX_BODY_BYTES + 1) + b"}"
    response = client.post(
        "/v1/evaluate", content=big, headers={"content-type": "application/json"}
    )
    assert response.status_code == 413


def test_oversized_streamed_bodies_are_rejected(client):
    def chunks():
        for _ in range(5):
            yield b" " * (MAX_BODY_BYTES // 4)

    response = client.post(
        "/v1/evaluate", content=chunks(), headers={"content-type": "application/json"}
    )
    assert response.status_code == 413


def test_bad_content_length_is_rejected(client):
    response = client.post("/v1/evaluate", content=b"{}", headers={"content-length": "abc"})
    assert response.status_code in {400, 413}


def test_security_headers_on_every_response(client):
    for response in (client.get("/v1/meta"), client.get("/missing")):
        assert response.headers["content-security-policy"] == CONTENT_SECURITY_POLICY
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["referrer-policy"] == "no-referrer"
        assert response.headers["x-frame-options"] == "DENY"
    assert client.get("/v1/meta").headers["cache-control"] == "no-store"


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_api_docs_are_disabled(client, path):
    assert client.get(path).status_code == 404


def test_unexpected_errors_are_generic():
    def explode(_facts, _data):
        raise RuntimeError(SSN_LIKE_VALUE)

    registry = RuleRegistry([RuleSet(data=rule_data(), logic=explode)])
    app = create_app(rules=registry, policies={"baseline": BASELINE})
    client = TestClient(app, client=LOCAL, raise_server_exceptions=False)
    response = _evaluate(client)
    assert response.status_code == 500
    assert response.json() == {"error": "internal_error"}
    assert SSN_LIKE_VALUE not in response.text


def test_built_ui_is_served_when_present(tmp_path):
    (tmp_path / "index.html").write_text("<!doctype html><title>ok</title>")
    app = create_app(policies={"baseline": BASELINE}, static_dir=tmp_path)
    client = TestClient(app, client=LOCAL)
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>ok</title>" in response.text
    assert response.headers["content-security-policy"] == CONTENT_SECURITY_POLICY


def test_defaults_use_packaged_rules_and_baseline_policy():
    client = TestClient(create_app(), client=LOCAL)
    assert [p["id"] for p in client.get("/v1/meta").json()["policies"]] == ["baseline"]
    response = _evaluate(client, {"policy": "baseline", "facts": facts_payload()})
    assert response.json()["decision"]["reasons"] == ["unsupported_jurisdiction"]


# ── Middleware edge cases (non-HTTP traffic such as server lifespan events) ──


def _run_asgi(middleware, scope):
    seen = []

    async def inner(scope, receive, send):
        seen.append(scope["type"])
        if scope["type"] == "http":
            message = await receive()
            seen.append(message["type"])
            seen.append((await receive())["type"])
            await send({"type": "http.response.start", "status": 200, "headers": []})

    async def receive():
        return {"type": "http.request", "body": b"{}", "more_body": False}

    async def send(message):
        seen.append(message)

    import asyncio  # noqa: PLC0415

    asyncio.run(middleware(inner)(scope, receive, send))
    return seen


@pytest.mark.parametrize("middleware", [BodyLimitMiddleware, SecurityHeadersMiddleware])
def test_middleware_passes_non_http_scopes_through(middleware):
    assert _run_asgi(middleware, {"type": "lifespan"}) == ["lifespan"]


def test_body_limit_replays_the_body_once_then_disconnects():
    seen = _run_asgi(BodyLimitMiddleware, {"type": "http", "headers": [], "path": "/v1/x"})
    assert seen[:3] == ["http", "http.request", "http.disconnect"]


def test_scope_without_client_is_not_loopback():
    assert is_loopback({"type": "http"}) is False
    assert is_loopback({"type": "http", "client": ("::1", 1)}) is True
