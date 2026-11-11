# Translation review prompt

Conservatively edit the supplied Russian translation against the frozen English source. Produce a complete revised C1 text, preserving acceptable prose unchanged.

## Review rules

- Apply the non-negotiable translation rules in `prompts/translate.md`.
- Report additions, omissions, factual or meaning shifts, structural distortions, and clear Russian naturalness problems separately.
- Do not call a stylistic preference an error without source evidence.
- Do not invent context or resolve ambiguous source wording without evidence.
- Correct demonstrated grammar, terminology, meaning, and naturalness problems with the smallest justified change. Preserve natural word order, successful metaphors, character voice, register, narrative rhythm, uncertainty, point of view, and emotional intensity. Do not simplify metaphors, embellish, or make broad stylistic substitutions.
- Address user-reported or passage-specific issues when supplied, but only where the source and context support a correction.
- Check each material edit against its English source span and surrounding context. Keep unchanged all text without a justified correction.
- Review the full chapter for context, but quote only spans needed for the concise change log or unresolved questions.

## Decision for each finding

- **KEEP** — no change is supported; retain the current translation.
- **REVISE** — a source-supported error or clear naturalness problem merits one minimal change.
- **FLAG** — a possible issue is uncertain, depends on missing context or terminology, or needs a human decision; do not revise it.

For every **REVISE** or **FLAG** decision, record:

1. Source paragraph number and exact source span.
2. Exact current translation span.
3. Issue type and severity (minor / material / critical).
4. A concise explanation tied to the source evidence.
5. For **REVISE** only, the minimal replacement span applied in C1.

Use **KEEP** when a plausible alternative is only a stylistic preference. Return, in this order:

1. **Complete C1 Russian chapter text**, retaining acceptable wording and structure unchanged and applying only justified revisions. If no corrections are justified, reproduce the supplied translation unchanged.
2. **Concise change log** for applied revisions: source paragraph number, issue type, source evidence, and reason. Do not repeat unchanged spans.
3. **Unresolved questions** as separate **FLAG** items with source paragraph, exact English and Russian spans, and what needs human judgment. Do not implement an uncertain change. If none remain, say “None.”

## Required C1 integrity check

Before finalizing C1, compare every correction recorded as applied in the change log with the complete C1 at the corresponding source location. Confirm that the replacement is present and the superseded C0 wording is no longer there. Every correction recorded as applied must be present in C1, or explicitly documented as rejected or superseded with a reason; do not describe a correction as applied if it was not made. If any check fails, correct C1 and verify again. Also compare the complete C1 with C0 so unlogged changes are identified. Do not advance to rubric assessment or chapter acceptance until this check passes.

Do not include a general quality rating, preface, or stylistic rewrites. Literary ratings and the full fidelity assessment belong to the separate mandatory `prompts/assess.md` stage after C1; this review's defect log remains focused on actionable edits and flags. Return no English chapter text beyond the short evidence spans needed in the log or flags.

## Frozen English source

{{SOURCE_TEXT}}

## Initial Russian translation

{{TRANSLATION}}
