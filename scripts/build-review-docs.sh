#!/usr/bin/env bash
# Build one Word document per state for attorney review, from the Markdown specs.
# The Markdown files in docs/rules/<STATE>/ are the source of truth; rerun this after editing them.
# Usage: scripts/build-review-docs.sh [YYYY-MM-DD]   (requires pandoc)
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
prepared="${1:-$(date +%Y-%m-%d)}"
reference="$root/scripts/review-reference.docx"
work="$(mktemp -d "${TMPDIR:-/tmp}/review-docs.XXXXXX")"
trap 'rm -rf "$work"' EXIT

build() {
  local state="$1" name="$2" law_questions="$3" source_note="$4"
  local dir="$root/docs/rules/$state" combined="$work/$state.md"
  {
    cat <<COVER
---
title: "$name Deceased-Account Entitlement Rules"
subtitle: "Draft for attorney review"
date: "Prepared $prepared"
---

# How to review this document

**Status:** draft, not yet reviewed by an attorney. Nothing in this document is used by the decision engine until an attorney approves it.

**What we are asking you to do:**

1. Confirm each rule and its citation in Part 1, or correct it.
2. Answer the open questions marked **Law** in Part 2 ($law_questions). Questions marked **Owner**, **Policy**, or **Terms** are for the business; you may comment on them.
3. Confirm the expected outcome of each draft golden scenario at the end of Part 1. These scenarios become the engine's tests.

**How to respond:** turn on Track Changes and edit this document directly, or add comments. Please return it to the product owner.

**Sources:** $source_note See Part 3.

**Contents:** Part 1, rule specification. Part 2, open questions. Part 3, sources.

COVER
    for part in spec open-questions sources; do
      echo
      echo '```{=openxml}'
      echo '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
      echo '```'
      echo
      # Cross-file links become plain references to the parts of this document.
      sed -E \
        -e 's/\[sources\]\(sources\.md\)/Part 3/g' \
        -e 's/\[open-questions\.md\]\(open-questions\.md\)/Part 2/g' \
        -e 's/\[analysis below\]\(#[a-z0-9-]+\)/analysis at the end of Part 2/g' \
        "$dir/$part.md"
    done
  } > "$combined"
  pandoc "$combined" --from gfm+yaml_metadata_block+raw_attribute --to docx \
    --reference-doc "$reference" --output "$dir/$state-attorney-review.docx"
  echo "wrote docs/rules/$state/$state-attorney-review.docx"
}

# Legal research reviews: landscape (wide tables). The first "# " heading becomes the title.
build_research() {
  local source="$1" title="$2" output="$3" combined="$work/research.md"
  {
    printf -- '---\ntitle: "%s"\nsubtitle: "Legal research for attorney verification. Not legal advice."\ndate: "Prepared %s"\n---\n\n' "$title" "$prepared"
    awk 'BEGIN { skipped = 0 } /^# / && !skipped { skipped = 1; next } { print }' "$root/$source"
  } > "$combined"
  pandoc "$combined" --from gfm+yaml_metadata_block --to docx \
    --reference-doc "$root/scripts/review-reference-landscape.docx" --output "$root/$output"
  echo "wrote $output"
}

build CA "California" "Q2, Q3, Q5, Q6, Q8, Q9" \
  "The official California code site blocked automated retrieval, so statute text was read from a public mirror of it. Every citation must be confirmed against leginfo.legislature.ca.gov (question Q9). Dollar limits come from the Judicial Council's official § 890 list."
build WA "Washington" "W2, W3, W4, W5, W6, W9, W10" \
  "All statute text was read from the official Revised Code of Washington at app.leg.wa.gov."

for review in \
  "docs/rules/CA/legal-review.md|California Legal Research Review|docs/rules/CA/CA-legal-research-review.docx" \
  "docs/rules/WA/legal-review.md|Washington Legal Research Review|docs/rules/WA/WA-legal-research-review.docx" \
  "docs/rules/legal-risk-review.md|Legal Risk and Edge-Case Review|docs/rules/legal-risk-review.docx"; do
  IFS='|' read -r source title output <<< "$review"
  if [ -f "$root/$source" ]; then build_research "$source" "$title" "$output"; fi
done
