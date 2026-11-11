# Minimal scene analysis prompt

Analyze only the supplied frozen English scene and its adjacent source context. Return a concise Markdown analysis for use during translation; do not translate or rewrite any source text.

## Evidence rules

- Ground every factual statement in a source paragraph number and a short source span.
- Separate explicit facts from interpretation. Label uncertainty rather than resolving it.
- Do not import canon, outside plot knowledge, or information absent from the supplied text.
- Do not infer motives, diagnoses, relationship history, or emotions beyond what the source supports.
- Keep the analysis compact and limited to events, participants and relevant relationships, emotional dynamics, and source style.

## Scene and context

{{SCENE_AND_CONTEXT}}

## Dynamic Context (optional)

{{DYNAMIC_CONTEXT}}

Use this compact prior-story record only as continuity aid. The current English scene takes precedence if anything conflicts. Cite either current source paragraph/span or the earlier chapter and evidence recorded in Dynamic Context; keep established facts, interpretations, and unresolved questions distinct. Ignore this section when Dynamic Context is disabled by request.
