"""FastAPI application: evaluate one case, list policies, report engine metadata."""

from collections.abc import Mapping
from importlib.metadata import version
from pathlib import Path
from typing import Annotated, Final

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, StringConstraints, ValidationError

from decision_engine.api.guards import (
    BodyLimitMiddleware,
    LocalOnlyMiddleware,
    SecurityHeadersMiddleware,
    require_local_client,
)
from decision_engine.core import (
    Facts,
    InstitutionPolicy,
    RuleRegistry,
    canonical_json,
    evaluate,
    sha256_hex,
)
from decision_engine.core.decision import DECISION_SCHEMA_VERSION
from decision_engine.core.facts import FACTS_SCHEMA_VERSION
from decision_engine.rules_loader import default_policy, default_registry
from decision_engine.safe_errors import safe_errors

PACKAGE: Final = "decision-engine"

PolicyKey = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]{1,62}$")]


class EvaluateRequest(BaseModel):
    """One case: the facts and which institution policy to apply."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    policy: PolicyKey
    facts: Facts


def create_app(
    *,
    rules: RuleRegistry | None = None,
    policies: Mapping[str, InstitutionPolicy] | None = None,
    static_dir: Path | None = None,
) -> FastAPI:
    """Build the local app.

    Args:
        rules: Rule registry; defaults to the packaged rules.
        policies: Policies by institution ID; defaults to the packaged baseline only.
        static_dir: Built UI to serve at ``/``; omitted when it does not exist.
    """
    registry = rules or default_registry()
    available = dict(policies) if policies is not None else _baseline_only()
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.include_router(_router(registry, available))
    if static_dir is not None and static_dir.is_dir():
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="ui")
    app.add_exception_handler(Exception, _internal_error)
    # Outermost first at request time: local check, then body cap, then headers.
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(BodyLimitMiddleware)
    app.add_middleware(LocalOnlyMiddleware)
    return app


def _baseline_only() -> dict[str, InstitutionPolicy]:
    baseline = default_policy()
    return {baseline.institution: baseline}


def _router(rules: RuleRegistry, policies: Mapping[str, InstitutionPolicy]) -> APIRouter:
    router = APIRouter(prefix="/v1", dependencies=[Depends(require_local_client)])

    @router.get("/meta")
    def meta() -> dict[str, object]:
        """Engine and schema versions, rule registry hash, and the policies on offer."""
        return {
            "engine_version": version(PACKAGE),
            "facts_schema_version": FACTS_SCHEMA_VERSION,
            "decision_schema_version": DECISION_SCHEMA_VERSION,
            "registry_hash": rules.registry_hash,
            "policies": [
                {
                    "id": key,
                    "institution": policy.institution,
                    "version": policy.version,
                    "description": policy.description,
                }
                for key, policy in sorted(policies.items())
            ],
        }

    @router.post("/evaluate")
    async def evaluate_case(request: Request) -> Response:
        """Evaluate one case. The body is parsed in strict JSON mode, like the CLI."""
        try:
            case = EvaluateRequest.model_validate_json(await request.body())
        except ValidationError as error:
            return JSONResponse(status_code=422, content={"errors": safe_errors(error)})
        policy = policies.get(case.policy)
        if policy is None:
            raise HTTPException(status_code=404, detail="unknown_policy")
        decision = evaluate(case.facts, rules, policy)
        envelope = {
            "decision": decision.model_dump(mode="json"),
            "facts_hash": sha256_hex(case.facts),
            "engine_version": version(PACKAGE),
        }
        return Response(canonical_json(envelope), media_type="application/json")

    return router


async def _internal_error(_request: Request, _error: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": "internal_error"})
