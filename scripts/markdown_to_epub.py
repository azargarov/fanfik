#!/usr/bin/env python3
"""Assemble Markdown chapter files into a small EPUB 3 ebook.

Example:
  python3 scripts/markdown_to_epub.py -o book.epub \
      --title "Example Book" --author "A. Writer" ch01.md ch02.md

A top-level Markdown heading becomes the chapter title and is rendered once.
Without one, a title is derived from common chapter filename patterns or the
filename stem. Chapters are emitted in the order supplied.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET


def _inline(text: str) -> str:
    """Render a useful, deliberately small subset of inline Markdown as XHTML."""
    # Escape raw input first, then safely introduce tags for recognized syntax.
    text = html.escape(text, quote=False)
    code: list[str] = []

    def hold(match: re.Match[str]) -> str:
        code.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(code) - 1}\x00"

    text = re.sub(r"`([^`]+)`", hold, text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", lambda m: '<a href="' + m.group(2).replace('"', '&quot;') + '">' + m.group(1) + '</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*|__([^_]+)__", lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)", lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)
    for i, fragment in enumerate(code):
        text = text.replace(f"\x00{i}\x00", fragment)
    return text


def _title_for(path: Path, first_heading: str | None) -> str:
    if first_heading:
        return first_heading
    stem = path.stem
    match = re.fullmatch(r"(?:ch(?:apter)?[-_ ]?)(\d+)(?:[-_ ].*)?", stem, flags=re.I)
    if match:
        return f"Chapter {int(match.group(1))}"
    return stem.replace("_", " ").replace("-", " ").strip().title() or "Chapter"


def render_markdown(markdown: str, title: str) -> str:
    """Convert chapter Markdown blocks into valid, basic XHTML."""
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    in_code = False
    code_lines: list[str] = []

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            blocks.append(f"</{list_kind}>")
            list_kind = None

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{_inline(' '.join(part.strip() for part in paragraph))}</p>")
            paragraph.clear()

    title_used = False
    for line in lines:
        if line.strip().startswith("```"):
            flush_paragraph(); close_list()
            if in_code:
                blocks.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            flush_paragraph(); close_list()
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            flush_paragraph(); close_list()
            text = heading.group(2).strip()
            if not title_used and heading.group(1) == "#" and text == title:
                title_used = True
            else:
                level = len(heading.group(1))
                blocks.append(f"<h{level}>{_inline(text)}</h{level}>")
            continue
        if re.match(r"^\s*(---+|\*\*\*+|___+)\s*$", line):
            flush_paragraph(); close_list(); blocks.append("<hr />"); continue
        quote = re.match(r"^\s*>\s?(.*)$", line)
        if quote:
            flush_paragraph(); close_list()
            blocks.append(f"<blockquote><p>{_inline(quote.group(1))}</p></blockquote>")
            continue
        bullet = re.match(r"^\s*[-+*]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or ordered:
            flush_paragraph()
            kind = "ul" if bullet else "ol"
            if list_kind != kind:
                close_list(); blocks.append(f"<{kind}>"); list_kind = kind
            item = (bullet or ordered).group(1)
            blocks.append(f"<li>{_inline(item)}</li>")
            continue
        close_list()
        paragraph.append(line)
    flush_paragraph(); close_list()
    if in_code:
        raise ValueError("unclosed fenced code block")
    return (f'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru">'
            f"<head><title>{html.escape(title)}</title><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" /></head>"
            f"<body><h1>{html.escape(title)}</h1>{''.join(blocks)}</body></html>")


def _parse_chapter(path: Path) -> tuple[str, str]:
    if not path.exists():
        raise ValueError(f"chapter file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"chapter path is not a file: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"cannot read chapter file {path}: {exc}") from exc
    heading_match = re.search(r"(?m)^#\s+(.+?)\s*#*\s*$", text)
    title = _title_for(path, heading_match.group(1).strip() if heading_match else None)
    if not text.strip():
        raise ValueError(f"chapter file is empty: {path}")
    return title, text


def build_epub(chapter_paths: list[Path], output: Path, *, title: str,
               author: str, language: str = "ru") -> Path:
    """Build EPUB 3 from ordered UTF-8 Markdown chapter files."""
    if not chapter_paths:
        raise ValueError("provide at least one chapter file")
    if not title.strip() or not author.strip() or not language.strip():
        raise ValueError("book title, author, and language must not be empty")
    if Path(output).suffix.lower() != ".epub":
        raise ValueError("output path must use the .epub extension")
    chapters = [_parse_chapter(Path(path)) for path in chapter_paths]
    # Ensure XHTML uses the configured language, including for non-Russian books.
    rendered = []
    for index, (chapter_title, markdown) in enumerate(chapters, 1):
        xhtml = render_markdown(markdown, chapter_title).replace('xml:lang="ru"', f'xml:lang="{html.escape(language)}"')
        rendered.append((f"chapter{index:03d}.xhtml", chapter_title, xhtml))

    ns = "http://www.idpf.org/2007/opf"
    dc = "http://purl.org/dc/elements/1.1/"
    ET.register_namespace("", ns); ET.register_namespace("dc", dc); ET.register_namespace("dcterms", "http://purl.org/dc/terms/")
    package = ET.Element(f"{{{ns}}}package", {"version":"3.0", "unique-identifier":"book-id", "prefix":"dcterms: http://purl.org/dc/terms/"})
    metadata = ET.SubElement(package, f"{{{ns}}}metadata")
    ET.SubElement(metadata, f"{{{dc}}}identifier", {"id":"book-id"}).text = "urn:uuid:" + str(uuid.uuid4())
    ET.SubElement(metadata, f"{{{dc}}}title").text = title.strip()
    ET.SubElement(metadata, f"{{{dc}}}creator").text = author.strip()
    ET.SubElement(metadata, f"{{{dc}}}language").text = language.strip()
    ET.SubElement(metadata, f"{{{ns}}}meta", {"property":"dcterms:modified"}).text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = ET.SubElement(package, f"{{{ns}}}manifest")
    ET.SubElement(manifest, f"{{{ns}}}item", {"id":"nav", "href":"nav.xhtml", "media-type":"application/xhtml+xml", "properties":"nav"})
    ET.SubElement(manifest, f"{{{ns}}}item", {"id":"css", "href":"style.css", "media-type":"text/css"})
    for i, (name, _, _) in enumerate(rendered, 1):
        ET.SubElement(manifest, f"{{{ns}}}item", {"id":f"c{i}", "href":name, "media-type":"application/xhtml+xml"})
    spine = ET.SubElement(package, f"{{{ns}}}spine")
    for i in range(1, len(rendered)+1):
        ET.SubElement(spine, f"{{{ns}}}itemref", {"idref":f"c{i}"})
    opf = ET.tostring(package, encoding="utf-8", xml_declaration=True)

    nav_items = "".join(f'<li><a href="{name}">{html.escape(ch_title)}</a></li>' for name, ch_title, _ in rendered)
    nav = ('<?xml version="1.0" encoding="utf-8"?>'
           '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
           f'xml:lang="{html.escape(language)}"><head><title>Contents</title></head><body>'
           '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>' + nav_items + '</ol></nav></body></html>')
    container = ('<?xml version="1.0" encoding="UTF-8"?>'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/>'
                 '</rootfiles></container>')
    css = "body { font-family: serif; line-height: 1.45; } p { margin: 0 0 0.8em; } h1 { page-break-before: always; }"
    output = Path(output)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w") as archive:
            archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            archive.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr("OEBPS/package.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr("OEBPS/style.css", css, compress_type=zipfile.ZIP_DEFLATED)
            for name, _, xhtml in rendered:
                archive.writestr(f"OEBPS/{name}", xhtml, compress_type=zipfile.ZIP_DEFLATED)
    except OSError as exc:
        raise ValueError(f"cannot write EPUB {output}: {exc}") from exc
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assemble ordered Markdown chapters into an EPUB 3 ebook.")
    parser.add_argument("chapters", nargs="+", type=Path, help="ordered UTF-8 Markdown chapter files")
    parser.add_argument("-o", "--output", required=True, type=Path, help="output .epub path")
    parser.add_argument("--title", required=True, help="book title")
    parser.add_argument("--author", required=True, help="book author")
    parser.add_argument("--language", default="ru", help="BCP 47 language tag (default: ru)")
    args = parser.parse_args(argv)
    try:
        result = build_epub(args.chapters, args.output, title=args.title, author=args.author, language=args.language)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Created {result} ({len(args.chapters)} chapters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
