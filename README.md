# decisionengine

Deterministic, statute-cited entitlement decision engine for deceased customers' financial accounts (v1: California and Washington). See `ARCHITECTURE.md`.

```sh
uv sync --locked
uv run pytest --cov
uv run decision-engine evaluate facts.json
uv run decision-engine golden golden/   # attorney-readable scenario table
```
