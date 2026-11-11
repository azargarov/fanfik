# Fanfik

Fanfik translates English fiction from EPUB to Russian EPUB. In the recommended **Agent mode**, Codex or another filesystem-capable coding agent prepares the source, runs the required chapter stages in order, records resumable progress, and assembles the final book after every chapter is accepted. **Chat mode** is available when an LLM cannot access files; the user manually supplies text, manages checkpoints, and runs conversion commands.

[Getting started](docs/GETTING_STARTED.md) · [Русский](README.ru.md)

## Quick start

1. Open this repository in Codex or a filesystem-capable coding agent and put one ordinary, unencrypted English EPUB in `books/`.
2. Ask: **“Read and follow `AGENTS.md`. Translate the English EPUB in `books/` into Russian using Fanfik. Save the finished EPUB in `books/`.”**
3. The agent prepares and checks the source, then completes every chapter in order: analysis, fresh C0 translation, editorial review and C1, C1 integrity verification, rubric assessment, required fidelity corrections and reassessment, acceptance, and Dynamic Context update. After all chapters pass, it exports and structurally validates the Russian EPUB. It asks only if the source, metadata, or a material ambiguity prevents safe progress.

Even for a whole-book request, Agent mode processes one chapter at a time rather than sending the entire book as one translation task. This keeps each stage within the model context window and supports checkpoint recovery. No separate stage or chapter requests are needed. Python 3.10+ is required for the included EPUB utilities; they use the standard library. The complete workflow is defined in [AGENTS.md](AGENTS.md); stage prompts and evaluation criteria are in [prompts/](prompts/) and [evaluation/rubric.md](evaluation/rubric.md). See [Getting started](docs/GETTING_STARTED.md) for both modes and the step-by-step Chat mode guide. Individual prompts can also be used manually for short passages.

## Files and resuming

Book-specific source, working files, progress checkpoints, and final EPUBs belong under `books/`, which is excluded from Git. The English EPUB is left unchanged. If a run is interrupted, reopen the repository in Codex and ask it to continue the translation in `books/`; it reads the progress record and existing artifacts, then resumes at the first incomplete stage.

## Scope and limitations

The importer supports text in ordinary EPUB 2/3 XHTML/HTML. It does not support PDF, OCR, DRM, images, or complex layout; extraction warnings and uncertain chapter boundaries require inspection. The workflow is coordinated by repository instructions and prompts and executed by the filesystem-capable agent, not by a standalone translation engine. Model review and single-candidate assessment are not independent validation, and Dynamic Context is experimental; its effect on quality has not been established. The EPUB builder handles a limited Markdown subset and checks structure, not literary quality.

Keep copyrighted or private source books and all generated book material out of version control. Text is processed by the AI provider used with Codex; check the provider’s data-handling terms.

## Repository map

- [AGENTS.md](AGENTS.md) — workflow, acceptance, recovery, and export rules
- [prompts/](prompts/) and [evaluation/rubric.md](evaluation/rubric.md) — stage instructions and criteria
- [scripts/epub_to_markdown.py](scripts/epub_to_markdown.py) — source extraction
- [scripts/markdown_to_epub.py](scripts/markdown_to_epub.py) — EPUB assembly
- [ROADMAP.md](ROADMAP.md) — prototype status, limitations, and future directions
