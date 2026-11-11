# Research backlog

All items below are deferred. They are questions for possible future work, not approved experiments or promised capabilities. Any work should be explicitly requested, limited to a clear question, and evaluated without treating model self-review as independent evidence.

## Translation context and continuity

Test whether brief, verified, as-of-scene context helps a passage whose interpretation demonstrably depends on earlier events, compared with the adjacent source text alone. Keep facts, interpretations, and uncertainty distinct; exclude later revelations. Do not build persistent narrative-state machinery unless simple manual notes show repeatable value.

## Independent quality assessment

Develop a credible source-grounded review procedure, ideally with blind bilingual human assessment where available. Examine omissions, additions, meaning shifts, attribution, uncertainty, and unnecessary edits separately from stylistic preferences. Do not use model KEEP/ACCEPT judgments alone as proof of quality.

## Conservative literary editing

Assess how minimal change thresholds, ambiguity flags, terminology decisions, and dialogue layout affect source fidelity and reader experience. Preserve competing judgments where a choice remains uncertain; do not turn an isolated preference into a global replacement rule.

## Reusable tooling, only if a repeated need is shown

- Context extraction and verification, measured separately from whether context helps.
- Lightweight terminology and editorial-decision notes for recurring continuity problems.
- Selective review or chapter-continuity support when manual work reveals a specific recurring gap.
- Reproducible comparisons of model roles only when the task, access, and evaluation material are comparable.

Do not assume these require automated pipelines, databases, agents, services, or large benchmarks. The current EPUB builder is a narrow formatting utility and makes no claim about whole-book workflow support.

## Decision rules

- Treat the English source as authoritative and preserve ambiguity, voice, structure, and restraint.
- Distinguish observed evidence, interpretation, and unverified hypothesis.
- Keep tests small and falsifiable; inconclusive or negative results are valid outcomes.
- Retain existing acceptable text unless a source-grounded issue is established.
