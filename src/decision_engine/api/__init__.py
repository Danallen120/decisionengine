"""Local HTTP API and UI host (REQ-API-001): a thin layer over the pure core.

Every request must come from the local machine. That is enforced twice: by an
ASGI middleware that covers the UI files too, and by a router-level dependency
on every ``/v1`` route, so a new route cannot ship unguarded. Production
authentication is still TO BE DECIDED (ARCHITECTURE.md); this guard stands in
for it while the tool runs locally.

Request bodies and decisions are never logged.
"""

from decision_engine.api.app import create_app

__all__ = ["create_app"]
