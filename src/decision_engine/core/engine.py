"""The decision function (REQ-CORE-003).

``evaluate`` is pure: the same facts and the same registry always produce an
equal ``Decision``. It performs no I/O and never reads a clock or a random
source; rule data is loaded by an outer layer and passed in.
"""

from decision_engine.core.decision import Decision, Determination, Outcome, ReasonCode
from decision_engine.core.facts import Facts
from decision_engine.core.rules import RuleRegistry


def evaluate(facts: Facts, rules: RuleRegistry) -> Decision:
    """Decide who may be paid for one account under the rule set covering the facts.

    Args:
        facts: Validated account facts.
        rules: Every loaded rule set.

    Returns:
        A determined decision, or a non-determinable one with reason codes when no
        rule set covers the facts or the covering rule set does not address them.
    """
    selected = rules.select(facts.jurisdiction, facts.date_of_death)
    if isinstance(selected, ReasonCode):
        return Decision(
            outcome=Outcome.NOT_DETERMINABLE,
            reasons=(selected,),
            registry_hash=rules.registry_hash,
        )
    result = selected.logic(facts, selected.data)
    if isinstance(result, Determination):
        return Decision(
            outcome=Outcome.DETERMINED,
            determination=result,
            rule_set=selected.ref(),
            registry_hash=rules.registry_hash,
        )
    return Decision(
        outcome=Outcome.NOT_DETERMINABLE,
        reasons=result.reasons,
        rule_set=selected.ref(),
        registry_hash=rules.registry_hash,
    )
