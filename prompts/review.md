# Translation review prompt

Conservatively edit the supplied Russian translation against the frozen English source. Produce a complete revised C1 text, preserving acceptable prose unchanged.

## Review rules

- Apply the non-negotiable translation rules in `prompts/translate.md`.
- Report additions, omissions, factual or meaning shifts, structural distortions, and clear Russian naturalness problems separately.
- Do not call a stylistic preference an error without source evidence.
- Do not invent context or resolve ambiguous source wording without evidence.
- Correct demonstrated grammar, terminology, meaning, and naturalness problems with the smallest justified change. Preserve natural word order, successful metaphors, character voice, register, narrative rhythm, uncertainty, point of view, and emotional intensity. Do not simplify metaphors, embellish, or make broad stylistic substitutions.
- Address reader-reported issues only where supported in context: potentially unnatural feminine forms of «эльф»; «первый рыдок» where «первый всхлип» fits the English; «повидать»/«проведать» according to context; excessive narrative em dashes; and dialogue paragraphing where a separate paragraph improves Russian readability. Also apply any explicitly supplied passage-specific correction.
- Treat examples as targets for judgment, not global replacement rules. Do not change every em dash, every dialogue/action paragraph, or every occurrence of a grammatical form automatically.
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

Do not include a general quality rating, preface, or stylistic rewrites. Return no English chapter text beyond the short evidence spans needed in the log or flags.

## Frozen English source

{{SOURCE_TEXT}}

## Initial Russian translation

{{TRANSLATION}}
