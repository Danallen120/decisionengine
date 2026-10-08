"""Validation errors reduced to field paths and error types, never submitted values."""

from typing import Final

from pydantic import ValidationError

MAX_LOC_PART_CHARS: Final = 64


def safe_errors(error: ValidationError) -> list[dict[str, object]]:
    """Field paths and error types only; never the offending input values."""
    return [
        {
            "loc": [
                part if isinstance(part, int) else str(part)[:MAX_LOC_PART_CHARS]
                for part in detail["loc"]
            ],
            "type": detail["type"],
        }
        for detail in error.errors(include_url=False, include_input=False, include_context=False)
    ]
