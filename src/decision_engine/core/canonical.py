"""Canonical JSON: one byte-exact text for equal values, used for hashing and output."""

import json
from hashlib import sha256

from pydantic import BaseModel


def canonical_json(value: object) -> str:
    """Serialize JSON-compatible data with sorted keys and no insignificant whitespace.

    ``BaseModel`` instances are dumped in JSON mode first, so ``Decimal``,
    ``Fraction``, and ``date`` values use their schema string forms.
    """
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(value: object) -> str:
    """SHA-256 of the canonical JSON form of ``value``."""
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()
