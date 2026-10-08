"""Value types shared by facts, decisions, and rule data.

Money and shares never use floats: money is a two-place ``Decimal`` parsed only
from strings, and shares are exact ``Fraction`` values serialized as ``"n/d"``.
"""

import re
from decimal import Decimal
from fractions import Fraction
from typing import Annotated, Final

from pydantic import PlainSerializer, PlainValidator, StringConstraints, WithJsonSchema

_MONEY_PATTERN: Final = re.compile(r"^(0|[1-9][0-9]{0,14})(\.[0-9]{1,2})?$")
_SHARE_PATTERN: Final = re.compile(r"^([1-9][0-9]{0,8})/([1-9][0-9]{0,8})$")
_CENTS: Final = Decimal("0.01")
_MONEY_JSON_PATTERN: Final = _MONEY_PATTERN.pattern
_SHARE_JSON_PATTERN: Final = _SHARE_PATTERN.pattern
_SHA256_HEX_PATTERN: Final = r"^[0-9a-f]{64}$"


def _parse_money(value: object) -> Decimal:
    """Accept a non-negative amount as a string (or an exact ``Decimal``), never a float or int."""
    if isinstance(value, Decimal):
        text = format(value, "f")
    elif isinstance(value, str):
        text = value
    else:
        msg = "money must be a decimal string such as '1234.56'"
        raise ValueError(msg)  # noqa: TRY004 - pydantic only reports ValueError as a validation error
    if not _MONEY_PATTERN.fullmatch(text):
        msg = "money must be a non-negative amount with at most 2 decimal places"
        raise ValueError(msg)
    return Decimal(text).quantize(_CENTS)


def _parse_share(value: object) -> Fraction:
    """Accept a share as an ``"n/d"`` string (or a ``Fraction``) in the range (0, 1]."""
    if isinstance(value, Fraction):
        share = value
    elif isinstance(value, str) and _SHARE_PATTERN.fullmatch(value):
        share = Fraction(value)
    else:
        msg = "share must be a fraction string such as '1/3'"
        raise ValueError(msg)
    if not 0 < share <= 1:
        msg = "share must be greater than 0 and at most 1"
        raise ValueError(msg)
    return share


def _format_share(share: Fraction) -> str:
    return f"{share.numerator}/{share.denominator}"


Money = Annotated[
    Decimal,
    PlainValidator(_parse_money),
    PlainSerializer(lambda amount: format(amount, "f"), return_type=str),
    WithJsonSchema({"type": "string", "pattern": _MONEY_JSON_PATTERN}),
]
"""Non-negative USD amount with exactly two decimal places once parsed."""

Share = Annotated[
    Fraction,
    PlainValidator(_parse_share),
    PlainSerializer(_format_share, return_type=str),
    WithJsonSchema({"type": "string", "pattern": _SHARE_JSON_PATTERN}),
]
"""Exact fractional share in (0, 1], always serialized as ``"numerator/denominator"``."""

Citation = Annotated[
    str,
    StringConstraints(min_length=3, max_length=200, pattern=r"^[A-Za-z0-9 .,;:()§'/-]+$"),
]
"""Statute citation, e.g. ``"Cal. Prob. Code § 13100"``."""

Sha256Hex = Annotated[str, StringConstraints(pattern=_SHA256_HEX_PATTERN)]
"""Lowercase hex SHA-256 digest."""

Code = Annotated[str, StringConstraints(pattern=r"^[A-Z][A-Z0-9_]{2,63}$")]
"""Stable machine-readable code, e.g. a required-document code."""

SemVer = Annotated[
    str,
    StringConstraints(pattern=r"^(0|[1-9][0-9]{0,3})\.(0|[1-9][0-9]{0,3})\.(0|[1-9][0-9]{0,3})$"),
]
"""Semantic version ``MAJOR.MINOR.PATCH``."""

InstitutionId = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]{1,62}$")]
"""Institution identifier for a policy, e.g. ``"baseline"``. Lowercase letters, digits, hyphens."""

PlainEnglish = Annotated[str, StringConstraints(min_length=10, max_length=500)]
"""A plain-English explanation written for attorney review."""
