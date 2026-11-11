# Public project roadmap

Fanfik currently provides reusable prompts, an assessment rubric, and a small EPUB assembly script. The workflow is human-directed: people supply source passages, select and provide relevant context, judge proposed revisions, and decide whether work is acceptable. Nothing in the repository performs end-to-end translation or autonomous acceptance.

## Established principles

- The supplied English source is authoritative; preserve facts, uncertainty, ambiguity, subtext, voice, register, pacing, structure, and emotional restraint.
- Prefer natural Russian without embellishing plain prose. Keep acceptable text unchanged and make the smallest source-grounded correction.
- Separate evidence-based fidelity defects from stylistic preferences and reader ratings. Model self-review is not independent validation.
- Existing trials were limited and did not establish general superiority for structured context, adaptive editing, or any model choice.

## Current reusable components

- Translation, scene-analysis, and conservative-review prompts in `prompts/`.
- A blind translation-assessment rubric in `evaluation/`.
- A Markdown-to-EPUB 3 builder in `scripts/`, with tests in `tests/`.

These components do not constitute a fully automated workflow. The EPUB builder supports basic Markdown only and does not assess content or translation quality.

## Deferred direction

Potential future research is recorded in [BACKLOG.md](BACKLOG.md). No candidate is active by default. Further work should be explicitly authorized, small, source-grounded, and evaluated against a clear question. Do not infer a general method from one book or a small number of model outputs.
