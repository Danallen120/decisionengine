"""REQ-UI-001: keep the UI in step with the engine, and keep it free of risky patterns."""

import re
from enum import StrEnum
from pathlib import Path

import pytest

from decision_engine.core import (
    AccountType,
    AdministrationStatus,
    AffiantCapacity,
    HolderRole,
    ReasonCode,
    Relationship,
)

FRONTEND = Path(__file__).parents[1] / "frontend"
SOURCES = sorted((FRONTEND / "src").rglob("*.ts*"))
TYPES_TS = (FRONTEND / "src" / "types.ts").read_text()
EXPLAIN_TS = (FRONTEND / "src" / "explain.ts").read_text()


def _ts_const_array(name: str) -> set[str]:
    match = re.search(rf"export const {name} = \[(.*?)\] as const;", TYPES_TS, re.DOTALL)
    assert match, f"{name} not found in types.ts"
    return set(re.findall(r'"([a-z_]+)"', match.group(1)))


@pytest.mark.parametrize(
    ("ts_name", "enum"),
    [
        ("RELATIONSHIPS", Relationship),
        ("ACCOUNT_TYPES", AccountType),
        ("HOLDER_ROLES", HolderRole),
        ("ADMINISTRATION_STATUSES", AdministrationStatus),
        ("AFFIANT_CAPACITIES", AffiantCapacity),
    ],
)
def test_form_options_match_engine_enums(ts_name: str, enum: type[StrEnum]):
    assert _ts_const_array(ts_name) == {member.value for member in enum}


def test_every_reason_code_has_a_plain_english_explanation():
    explained = set(re.findall(r"^  ([a-z_]+): \{", EXPLAIN_TS, re.MULTILINE))
    assert explained == {code.value for code in ReasonCode}


@pytest.mark.parametrize(
    "pattern",
    [
        r"dangerouslySetInnerHTML",
        r"\.innerHTML",
        r"\beval\(",
        r"new Function\(",
        r"localStorage",
        r"sessionStorage",
        r"indexedDB",
    ],
)
def test_ui_source_avoids_risky_apis(pattern: str):
    offenders = [
        p.name for p in SOURCES if re.search(pattern, p.read_text()) and ".test." not in p.name
    ]
    assert not offenders


def test_ui_loads_nothing_from_other_origins():
    files = [FRONTEND / "index.html", *SOURCES, FRONTEND / "src" / "styles.css"]
    offenders = [p.name for p in files if re.search(r"https?://(?!127\.0\.0\.1)", p.read_text())]
    assert not offenders
