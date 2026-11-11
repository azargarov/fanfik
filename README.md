# Fanfik — English-to-Russian literary translation

Fanfik is a small public project for human-directed literary translation. It collects source-faithful translation prompts, a concise scene-analysis prompt, a conservative review prompt, a blind-assessment rubric, and a utility for assembling Markdown chapters into an EPUB. It does not provide a fully automated translation or quality-assurance pipeline.

## What the project supports

- Translation guided by fidelity to the supplied source, natural Russian, authorial voice, and minimal editorial intervention.
- Compact, source-grounded scene analysis that distinguishes explicit facts from interpretation and uncertainty.
- Conservative review that records evidence for revisions and flags uncertain decisions.
- Blind assessment that separates source-grounded defects from reader ratings.
- EPUB 3 assembly from an explicitly ordered list of UTF-8 Markdown chapter files.

Prompts and evaluation materials: [prompts](prompts/translate.md), [scene analysis](prompts/analyze.md), [review](prompts/review.md), and the [assessment rubric](evaluation/rubric.md). Project status and future research candidates: [CURRENT.md](CURRENT.md), [ROADMAP.md](ROADMAP.md), and [BACKLOG.md](BACKLOG.md).

## Build an EPUB

With Python 3, run the builder and pass chapter files in reading order:

```sh
python3 scripts/markdown_to_epub.py -o book.epub \
  --title "Example Book" --author "A. Writer" ch01.md ch02.md
```

Each chapter must be a non-empty UTF-8 Markdown file. The builder uses a top-level heading as the chapter title, or derives one from the filename. It renders a limited Markdown subset; it does not translate or validate literary content. See [integration notes](docs/INTEGRATION.md) for its scope and input expectations.

## Project principles and limits

The English source is authoritative. Preserve meaning, uncertainty, subtext, structure, voice, and restraint; do not invent or embellish. Make only justified, source-grounded revisions, and retain uncertainty for human judgment. Model self-review is not independent validation.

Past project work did not establish a general quality advantage for added context or adaptive editing. Research ideas remain deferred in [BACKLOG.md](BACKLOG.md). This public repository intentionally contains no copyrighted source material, translations, or private experiment records.
