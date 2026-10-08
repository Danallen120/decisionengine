"""The decision function (REQ-CORE-003).

``evaluate`` is pure: the same facts, registry, and policy always produce an
equal ``Decision``. It performs no I/O and never reads a clock or a random
source; rule data and policy are loaded by an outer layer and passed in.
"""

from decision_engine.core.decision import (
    Decision,
    Determination,
    NotDeterminable,
    Outcome,
    ReasonCode,
)
from decision_engine.core.facts import Facts
from decision_engine.core.policy import InstitutionPolicy
from decision_engine.core.rules import RuleRegistry


def evaluate(facts: Facts, rules: RuleRegistry, policy: InstitutionPolicy) -> Decision:
    """Decide who may be paid for one account, under the law and the institution's policy.

    Args:
        facts: Validated account facts.
        rules: Every loaded rule set.
        policy: The institution policy; it can only make the decision stricter.

    Returns:
        A determined decision, or a non-determinable one with reason codes when no
        rule set covers the facts, the policy declines the case, or the covering
        rule set does not address the facts.
    """
    policy_ref = policy.ref()
    selected = rules.select(facts.jurisdiction, facts.date_of_death)
    if isinstance(selected, ReasonCode):
        return Decision(
            outcome=Outcome.NOT_DETERMINABLE,
            reasons=(selected,),
            policy=policy_ref,
            registry_hash=rules.registry_hash,
        )
    rule_set = selected.ref()
    result = (
        NotDeterminable(reasons=(ReasonCode.POLICY_DECLINED,))
        if policy.declines(facts)
        else selected.logic(facts, selected.data)
    )
    if isinstance(result, Determination):
        return Decision(
            outcome=Outcome.DETERMINED,
            determination=policy.apply(result),
            rule_set=rule_set,
            policy=policy_ref,
            registry_hash=rules.registry_hash,
        )
    return Decision(
        outcome=Outcome.NOT_DETERMINABLE,
        reasons=result.reasons,
        rule_set=rule_set,
        policy=policy_ref,
        registry_hash=rules.registry_hash,
    )
