# EPUB integration notes

## Codex book workflow

For a complete book translation, open the project in Codex, put the English EPUB in books/, and ask Codex to translate it. AGENTS.md coordinates source preparation, chapter analysis, translation, review, progress tracking, EPUB assembly, and structural validation. The scripts below perform conversion steps; there is no separate workflow engine. See [Getting Started](GETTING_STARTED.md).

### Experimental Dynamic Context

For ordinary multi-chapter translations, Codex maintains one compact `books/<book>/context.md` file. It is initialized before chapter one and updated only after the chapter passes editorial review and rubric assessment. It carries current character and relationship states, relevant established facts and history, terminology/style decisions, interpretations, and unresolved ambiguities into later analysis and translation. The current English source always takes precedence. Progress records which chapter the context represents so work can resume without applying an update twice; if progress and context disagree, Codex reconciles from accepted chapters before continuing. Users can explicitly request translation without Dynamic Context; that leaves analysis, review, and assessment in place. This feature is experimental, and its effect on translation quality has not been established. It does not change EPUB conversion or assembly.

## Preparing source text from EPUB

The standard command reads an ordinary, unencrypted EPUB 2/3 and writes one combined Markdown file and a JSON manifest beside the source:

    python3 scripts/epub_to_markdown.py books/example.epub

For an explicit destination directory:

    python3 scripts/epub_to_markdown.py books/example.epub --output-dir books/example/import

With the default command, the outputs are books/example.md and books/example.manifest.json. With --output-dir, the Markdown file is named after the EPUB stem and the manifest is manifest.json inside that directory. The converter follows the package spine, not filenames, skips spine documents with no extractable text, and reads archive entries without extracting them to disk. Existing output files are never overwritten.

The manifest records the source filename, title, spine reading order, archive paths, output filename, and warnings. The Markdown includes all text-bearing spine documents in order; Codex identifies story chapter boundaries and excludes recognizable navigation and front matter before translation. Multiple headings in a document and chapter boundaries spanning documents require careful inspection rather than automatic guesses.

Basic headings, paragraphs, dialogue text, emphasis, strong emphasis, horizontal rules, and Unicode text are retained where represented by ordinary XHTML/HTML elements. Table rows are separated by blank lines and cells by spaces, as plain text rather than Markdown tables. Image data, styling-dependent layout, scripts, and other complex content are not reproduced; warnings identify unsupported elements and flattened lists. The importer rejects unsafe ZIP paths, malformed package structure, unsupported spine media types, and EPUBs containing encrypted ZIP entries or encryption metadata. It does not bypass DRM. PDF and OCR are not supported.

## Assembling the Russian EPUB

The Markdown-to-EPUB builder accepts one or more non-empty UTF-8 Markdown files in reading order. Codex supplies reviewed chapter files in that order:

    python3 scripts/markdown_to_epub.py \
      --output book.ru.epub \
      --title "Example Book" --author "A. Writer" --language ru \
      chapters/ch01.c1.md chapters/ch02.c1.md

The title and author must be non-empty. Language defaults to ru. A first-level Markdown heading supplies each chapter title; otherwise the builder derives a title from a common chapter filename pattern or filename stem.

The renderer supports paragraphs, headings, lists, block quotes, fenced code, horizontal rules, emphasis, strong text, inline code, and HTTP(S) links. This is a limited Markdown subset, not a general renderer. The builder writes the requested path, so ensure it is unused before running it.

The builder does not translate, review, or validate literary fidelity; those stages are coordinated by Codex under AGENTS.md. The tests in ../tests/test_markdown_to_epub.py use synthetic input and require no copyrighted book content.
