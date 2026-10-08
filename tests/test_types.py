from decimal import Decimal
from fractions import Fraction

import pytest
from pydantic import TypeAdapter, ValidationError

from decision_engine.core.types import Money, Share

money = TypeAdapter(Money)
share = TypeAdapter(Share)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("0", "0.00"),
        ("12", "12.00"),
        ("12.5", "12.50"),
        ("999999999999999.99", "999999999999999.99"),
    ],
)
def test_money_parses_strings_to_two_places(raw, expected):
    assert money.dump_python(money.validate_python(raw), mode="json") == expected


def test_money_accepts_exact_decimal():
    assert money.validate_python(Decimal("1E+2")) == Decimal("100.00")


@pytest.mark.parametrize("raw", ["-1", "1.234", "01", "1e3", "", " 1", "1,000"])
def test_money_rejects_malformed_strings(raw):
    with pytest.raises(ValidationError):
        money.validate_python(raw)


@pytest.mark.parametrize("raw", [1.5, 100, True, None])
def test_money_rejects_non_strings(raw):
    with pytest.raises(ValidationError):
        money.validate_python(raw)


def test_money_rejects_json_number():
    with pytest.raises(ValidationError):
        money.validate_json("100.25")


@pytest.mark.parametrize(("raw", "expected"), [("1/3", Fraction(1, 3)), ("2/2", Fraction(1))])
def test_share_parses_fraction_strings(raw, expected):
    assert share.validate_python(raw) == expected


def test_share_serializes_as_fraction_string():
    assert share.dump_python(Fraction(1), mode="json") == "1/1"
    assert share.dump_python(Fraction(2, 6), mode="json") == "1/3"


@pytest.mark.parametrize("raw", ["0/1", "3/2", "1", "0.5", "-1/2", "1/0", 0.5, Fraction(0)])
def test_share_rejects_out_of_range_or_malformed(raw):
    with pytest.raises(ValidationError):
        share.validate_python(raw)
