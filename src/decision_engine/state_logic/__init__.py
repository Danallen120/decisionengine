"""Pure rule logic per state and rule-set version.

Each entry pairs with a data file in ``decision_engine/rules_data``. No state
rules exist yet; CA and WA arrive through their own requirements, with citations
reviewed by an attorney.
"""

from collections.abc import Mapping

from decision_engine.core import Jurisdiction
from decision_engine.core.rules import RuleLogic

LOGIC: Mapping[tuple[Jurisdiction, str], RuleLogic] = {}
