# Fanfik

Fanfik is a Codex-guided workflow for translating English fiction into Russian. It prepares an EPUB, works through chapters in order, records resumable progress, and assembles a Russian EPUB after each chapter passes review and assessment.

[Getting started](docs/GETTING_STARTED.md) · [Русский](README.ru.md)

## Quick start

1. Open this repository in Codex and put one ordinary, unencrypted English EPUB in `books/`.
2. Ask: **“Translate the English EPUB in `books/` into Russian using Fanfik. Save the finished EPUB in `books/`.”**
3. Codex prepares and checks the source, analyzes, translates, reviews, and assesses every chapter, then exports and structurally validates the Russian EPUB. It asks only if the source, metadata, or a material ambiguity prevents safe progress.

No separate chapter-by-chapter requests or Python packages are needed. Python 3.10+ is required for the included EPUB utilities. The complete workflow is defined in [AGENTS.md](AGENTS.md); stage prompts and evaluation criteria are in [prompts/](prompts/) and [evaluation/rubric.md](evaluation/rubric.md).

## Files and resuming

Book-specific source, working files, progress, and final EPUBs belong under `books/`, which is excluded from Git. The English EPUB is left unchanged. If a run is interrupted, reopen the repository in Codex and ask it to continue the translation in `books/`; it reads the progress record and existing artifacts, then resumes at the first incomplete stage.

## Scope and limitations

The importer supports text in ordinary EPUB 2/3 XHTML/HTML. It does not support PDF, OCR, DRM, images, or complex layout; extraction warnings and uncertain chapter boundaries require inspection. The workflow is coordinated by Codex instructions, not a standalone translation engine. Model review and single-candidate assessment are not independent validation, and Dynamic Context is experimental; its effect on quality has not been established. The EPUB builder handles a limited Markdown subset and checks structure, not literary quality.

Keep copyrighted or private source books and all generated book material out of version control. Text is processed by the AI provider used with Codex; check the provider’s data-handling terms.

## Repository map

- [AGENTS.md](AGENTS.md) — workflow, acceptance, recovery, and export rules
- [prompts/](prompts/) and [evaluation/rubric.md](evaluation/rubric.md) — stage instructions and criteria
- [scripts/epub_to_markdown.py](scripts/epub_to_markdown.py) — source extraction
- [scripts/markdown_to_epub.py](scripts/markdown_to_epub.py) — EPUB assembly
- [ROADMAP.md](ROADMAP.md) — prototype status, limitations, and future directions
