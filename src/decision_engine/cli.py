"""Command-line interface: a thin wrapper over the core (REQ-CLI-001).

Output is canonical decision JSON on stdout. Validation errors go to stderr as
field paths and error types only; input values are never echoed.
"""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import BinaryIO, Final, TextIO

from pydantic import ValidationError

from decision_engine.core import Facts, RuleRegistry, canonical_json, evaluate
from decision_engine.golden import load_scenarios, render_markdown
from decision_engine.rules_loader import default_registry

MAX_INPUT_BYTES: Final = 10 * 1024 * 1024
MAX_BATCH_ITEMS: Final = 1000
MAX_LOC_PART_CHARS: Final = 64

EXIT_OK: Final = 0
EXIT_SOME_INVALID: Final = 1
EXIT_INVALID_INPUT: Final = 2


class InputError(Exception):
    """Input was rejected before any evaluation."""


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return the process exit code."""
    args = _parser().parse_args(argv)
    try:
        if args.command == "golden":
            sys.stdout.write(render_markdown(load_scenarios(args.directory)))
            return EXIT_OK
        raw = _read_capped(args.input)
        rules = default_registry()
        if args.command == "evaluate":
            return _evaluate_one(raw, rules, sys.stdout, sys.stderr)
        return _evaluate_batch(raw, rules, sys.stdout)
    except InputError as error:
        _write_json(sys.stderr, {"error": str(error)})
        return EXIT_INVALID_INPUT


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="decision-engine", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("evaluate", "evaluate one fact set (a JSON object)"),
        ("batch", f"evaluate a JSON array of up to {MAX_BATCH_ITEMS} fact sets"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("input", help="JSON file path, or - for stdin")
    golden = commands.add_parser("golden", help="render golden scenarios for attorney review")
    golden.add_argument("directory", type=Path, help="directory of golden scenario YAML files")
    return parser


def _read_capped(source: str) -> bytes:
    if source == "-":
        return _read_stream(sys.stdin.buffer)
    with Path(source).open("rb") as stream:
        return _read_stream(stream)


def _read_stream(stream: BinaryIO) -> bytes:
    raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        msg = f"input exceeds {MAX_INPUT_BYTES} bytes"
        raise InputError(msg)
    return raw


def _evaluate_one(raw: bytes, rules: RuleRegistry, out: TextIO, err: TextIO) -> int:
    try:
        facts = Facts.model_validate_json(raw)
    except ValidationError as error:
        _write_json(err, {"errors": _safe_errors(error)})
        return EXIT_INVALID_INPUT
    out.write(canonical_json(evaluate(facts, rules)) + "\n")
    return EXIT_OK


def _evaluate_batch(raw: bytes, rules: RuleRegistry, out: TextIO) -> int:
    try:
        items = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        msg = "batch input is not valid JSON"
        raise InputError(msg) from error
    if not isinstance(items, list):
        msg = "batch input must be a JSON array"
        raise InputError(msg)
    if len(items) > MAX_BATCH_ITEMS:
        msg = f"batch exceeds {MAX_BATCH_ITEMS} items"
        raise InputError(msg)
    results: list[dict[str, object]] = []
    for index, item in enumerate(items):
        try:
            facts = Facts.model_validate_json(json.dumps(item))
        except ValidationError as error:
            results.append({"index": index, "errors": _safe_errors(error)})
            continue
        decision = evaluate(facts, rules).model_dump(mode="json")
        results.append({"index": index, "decision": decision})
    out.write(canonical_json(results) + "\n")
    has_errors = any("errors" in result for result in results)
    return EXIT_SOME_INVALID if has_errors else EXIT_OK


def _safe_errors(error: ValidationError) -> list[dict[str, object]]:
    """Field paths and error types only; never the offending input values."""
    return [
        {
            "loc": [
                part if isinstance(part, int) else str(part)[:MAX_LOC_PART_CHARS]
                for part in e["loc"]
            ],
            "type": e["type"],
        }
        for e in error.errors(include_url=False, include_input=False, include_context=False)
    ]


def _write_json(stream: TextIO, payload: object) -> None:
    stream.write(canonical_json(payload) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
