# decisionengine

Deterministic, statute-cited entitlement decision engine for deceased customers' financial accounts (v1: California and Washington). See `ARCHITECTURE.md`.

## Run the local tool

```sh
uv sync --locked
npm --prefix frontend ci && npm --prefix frontend run build   # builds the UI into the package
uv run decision-engine serve                                  # http://127.0.0.1:8000
```

The tool only accepts connections from this machine. Staff enter case facts in a guided form (no names or other personal information) and get a plain-English decision, or the reason it can't be decided, plus a downloadable record. Until a state's rules are approved by an attorney, every case returns "not determinable".

Offer institution policies alongside the statutory baseline with `--policies path/to/policies/`.

## Other commands

```sh
uv run pytest --cov
uv run decision-engine evaluate facts.json [--policy bank.yaml]
uv run decision-engine golden golden/   # attorney-readable scenario table
```
