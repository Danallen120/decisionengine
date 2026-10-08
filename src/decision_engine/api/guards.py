"""ASGI middleware for the local API: loopback-only access, body caps, security headers."""

from collections.abc import Awaitable, Callable, MutableMapping
from typing import Any, Final

from fastapi import HTTPException, Request

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]

LOOPBACK_HOSTS: Final = frozenset({"127.0.0.1", "::1"})
MAX_BODY_BYTES: Final = 256 * 1024

CONTENT_SECURITY_POLICY: Final = (
    "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
    "connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'none'; "
    "form-action 'self'; frame-ancestors 'none'"
)
_SECURITY_HEADERS: Final = (
    (b"content-security-policy", CONTENT_SECURITY_POLICY.encode()),
    (b"x-content-type-options", b"nosniff"),
    (b"referrer-policy", b"no-referrer"),
    (b"x-frame-options", b"DENY"),
    (b"cross-origin-opener-policy", b"same-origin"),
    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
)


def is_loopback(scope: Scope) -> bool:
    """Return whether the connection comes from this machine."""
    client = scope.get("client")
    if client is None:
        return False
    host: object = client[0]
    return host in LOOPBACK_HOSTS


async def require_local_client(request: Request) -> None:
    """Router-level dependency: deny every non-loopback caller (defense in depth)."""
    if not is_loopback(request.scope):
        raise HTTPException(status_code=403, detail="forbidden")


class LocalOnlyMiddleware:
    """Reject any HTTP request that does not come from the loopback interface."""

    def __init__(self, app: ASGIApp) -> None:
        """Wrap ``app``."""
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Pass loopback HTTP requests through; answer everything else with 403."""
        if scope["type"] == "http" and not is_loopback(scope):
            await _send_json(send, 403, b'{"error":"forbidden"}')
            return
        await self._app(scope, receive, send)


class BodyLimitMiddleware:
    """Reject request bodies over ``max_bytes`` before the app parses them."""

    def __init__(self, app: ASGIApp, max_bytes: int = MAX_BODY_BYTES) -> None:
        """Wrap ``app`` with a body cap of ``max_bytes``."""
        self._app = app
        self._max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Enforce the cap from Content-Length, then again while streaming."""
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return
        declared = dict(scope.get("headers", [])).get(b"content-length")
        if declared is not None and (not declared.isdigit() or int(declared) > self._max_bytes):
            await _send_json(send, 413, b'{"error":"body_too_large"}')
            return
        body = bytearray()
        more = True
        while more:
            message = await receive()
            body.extend(message.get("body", b""))
            more = message.get("more_body", False)
            if len(body) > self._max_bytes:
                await _send_json(send, 413, b'{"error":"body_too_large"}')
                return
        await self._app(scope, _replay(bytes(body)), send)


class SecurityHeadersMiddleware:
    """Add security headers to every response, and ``no-store`` to API responses."""

    def __init__(self, app: ASGIApp) -> None:
        """Wrap ``app``."""
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Inject headers into the response start message."""
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return
        is_api = str(scope.get("path", "")).startswith("/v1/")

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend(_SECURITY_HEADERS)
                if is_api:
                    headers.append((b"cache-control", b"no-store"))
                message["headers"] = headers
            await send(message)

        await self._app(scope, receive, send_with_headers)


def _replay(body: bytes) -> Receive:
    sent = False

    async def receive() -> Message:
        nonlocal sent
        if sent:
            return {"type": "http.disconnect"}
        sent = True
        return {"type": "http.request", "body": body, "more_body": False}

    return receive


async def _send_json(send: Send, status: int, body: bytes) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
                *_SECURITY_HEADERS,
            ],
        },
    )
    await send({"type": "http.response.body", "body": body})
