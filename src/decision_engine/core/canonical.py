"""Canonical JSON: one byte-exact text for equal values, used for hashing and output."""

import json

from pydantic import BaseModel


def canonical_json(value: object) -> str:
    """Serialize JSON-compatible data with sorted keys and no insignificant whitespace.

    ``BaseModel`` instances are dumped in JSON mode first, so ``Decimal``,
    ``Fraction``, and ``date`` values use their schema string forms.
    """
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
