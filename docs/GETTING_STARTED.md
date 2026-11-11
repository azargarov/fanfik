# Getting started

[Project README](../README.md) · [Русский](GETTING_STARTED.ru.md)

1. Open this repository in Codex. Python 3.10+ is needed for the bundled EPUB tools; they use the standard library.
2. Put one ordinary, unencrypted English EPUB in `books/`.
3. Ask Codex: **“Translate the English EPUB in `books/` into Russian using Fanfik. Save the finished EPUB in `books/`.”**

Codex prepares and checks the source, then analyzes, translates, reviews, and assesses chapters in order. It records progress, resumes at the first incomplete stage after interruption, and exports and structurally validates the Russian EPUB after all chapters are accepted. The source EPUB is not modified. All book files stay under `books/`, excluded from Git.

If several EPUBs are present and the intended source is unclear, Codex asks which to use. It also stops for extraction loss, unsafe chapter boundaries, required metadata it cannot determine, or a material unresolved ambiguity. You do not need to approve each chapter.

The importer supports ordinary text-based EPUB 2/3 XHTML/HTML. PDF, OCR, DRM, images, and complex layouts are unsupported. Codex checks warnings and chapter text, but model assessment is not independent translation validation. Dynamic Context is experimental and can be disabled by request.

For extraction and assembly command details, see [EPUB integration notes](INTEGRATION.md). The complete recovery and acceptance rules are in [AGENTS.md](../AGENTS.md).
