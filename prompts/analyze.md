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
