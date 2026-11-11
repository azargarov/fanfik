# EPUB builder integration notes

`../scripts/markdown_to_epub.py` assembles an explicitly ordered list of non-empty UTF-8 Markdown chapter files into a basic EPUB 3 ebook. It writes the output path supplied by the caller and creates its parent directory if needed.

## Inputs and behavior

- Pass chapter paths in reading order; the builder does not discover or sort files.
- Supply a non-empty title and author. Language defaults to `ru` and can be set with `--language`.
- A first-level Markdown heading supplies the chapter title; otherwise a common chapter filename pattern or filename stem is used.
- The renderer handles paragraphs, headings, lists, block quotes, fenced code, horizontal rules, emphasis, strong text, inline code, and HTTP(S) links. This is a limited subset, not a general Markdown implementation.

Example:

```sh
python3 scripts/markdown_to_epub.py -o book.epub \
  --title "Example Book" --author "A. Writer" --language ru \
  chapters/ch01.md chapters/ch02.md
```

The builder does not translate, review, validate literary fidelity, or automate a book workflow. The tests in `../tests/test_markdown_to_epub.py` exercise synthetic input; no copyrighted book content is required.
