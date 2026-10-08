# Rule data

One YAML file per state rule-set version, validated against `RuleSetData`
(`decision_engine/core/rules.py`). Every value needs a plain-English
description and at least one citation. Quote money values (`"1000.00"`) —
unquoted decimals are rejected.

Each file pairs with a logic entry in `decision_engine/state_logic`. No state
rules exist yet.
