#!/usr/bin/env python3
"""Convert an ordinary EPUB's spine documents to ordered Markdown chapters."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit
import zipfile
from xml.etree import ElementTree as ET


CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"
BLOCKS = {"p", "div", "section", "article", "blockquote", "li", "pre", "ul", "ol"}
HEADINGS = {f"h{i}" for i in range(1, 7)}


class _HTMLToMarkdown(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.warnings: list[str] = []
        self.has_heading = False
        self.heading_count = 0
        self._ignored_depth = 0

    def _break(self, count: int = 2) -> None:
        current = "".join(self.parts).rstrip()
        self.parts = [current] if current else []
        self.parts.append("\n" * count)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"head", "script", "style"}:
            self._ignored_depth += 1
            if tag != "head":
                self.warnings.append(f"{tag} element content omitted")
            return
        if self._ignored_depth:
            return
        if tag in BLOCKS or tag in HEADINGS:
            self._break()
        if tag in HEADINGS:
            self.has_heading = True
            self.heading_count += 1
            level = int(tag[1])
            self.parts.append("#" * level + " ")
        elif tag in {"em", "i", "cite", "dfn", "var"}:
            self.parts.append("*")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag == "br":
            self.parts.append("  \n")
        elif tag == "hr":
            self._break(); self.parts.append("---\n\n")
        elif tag == "tr":
            self._break()
        elif tag == "img":
            alt = dict(attrs).get("alt")
            if alt:
                self.parts.append(alt)
            self.warnings.append("image element encountered; image content was not extracted")
        elif tag in {"table", "svg", "video", "audio", "iframe", "math"}:
            self.warnings.append(f"{tag} element encountered; complex content may not be preserved")
        elif tag in {"ul", "ol"}:
            self.warnings.append(f"{tag} list encountered; list structure may be flattened")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"head", "script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._ignored_depth:
            return
        if tag in {"em", "i", "cite", "dfn", "var", "strong", "b"}:
            marker = "**" if tag in {"strong", "b"} else "*"
            self.parts.append(marker)
        elif tag in {"td", "th"}:
            self.parts.append(" ")
        elif tag in BLOCKS or tag in HEADINGS:
            self._break()

    def handle_data(self, data: str) -> None:
        if not data or self._ignored_depth:
            return
        # Collapse layout whitespace while retaining explicit element boundaries.
        cleaned = re.sub(r"\s+", " ", data)
        if cleaned:
            self.parts.append(cleaned)

    def handle_comment(self, data: str) -> None:
        return

    def result(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n" if text.strip() else ""


def _safe_archive_name(name: str) -> bool:
    if "\\" in name or name.startswith("/"):
        return False
    path = PurePosixPath(name)
    return not any(part in {"..", ""} for part in path.parts)


def _resolve_href(base: str, href: str) -> str:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        raise ValueError(f"external or unsupported EPUB resource: {href}")
    decoded = unquote(parsed.path)
    if not decoded or "\\" in decoded or decoded.startswith("/"):
        raise ValueError(f"invalid EPUB resource path: {href}")
    combined = posixpath.normpath(posixpath.join(posixpath.dirname(base), decoded))
    if combined == ".." or combined.startswith("../"):
        raise ValueError(f"EPUB resource escapes archive root: {href}")
    return combined


def _parse_document(content: bytes, label: str) -> ET.Element:
    try:
        return ET.fromstring(content)
    except ET.ParseError as exc:
        raise ValueError(f"malformed XML in {label}: {exc}") from exc


def _html_to_markdown(content: bytes, label: str, *, strict_xml: bool) -> tuple[str, bool, int, list[str]]:
    try:
        source = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"unsupported non-UTF-8 content in {label}: {exc}") from exc
    if strict_xml:
        _parse_document(content, label)
    parser = _HTMLToMarkdown()
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:
        raise ValueError(f"cannot parse XHTML/HTML {label}: {exc}") from exc
    return parser.result(), parser.has_heading, parser.heading_count, sorted(set(parser.warnings))


def convert_epub(epub_path: Path, output_dir: Path | None = None) -> dict[str, object]:
    epub_path = Path(epub_path)
    if not epub_path.is_file():
        raise ValueError(f"EPUB file does not exist: {epub_path}")
    output_dir = Path(output_dir) if output_dir is not None else None
    if output_dir is not None and output_dir.exists() and not output_dir.is_dir():
        raise ValueError(f"output directory is not a directory: {output_dir}")
    output_path = (output_dir / f"{epub_path.stem}.md") if output_dir is not None else epub_path.with_suffix(".md")
    manifest_path = (output_dir / "manifest.json") if output_dir is not None else output_path.with_name(f"{output_path.stem}.manifest.json")
    for target in (output_path, manifest_path):
        if target.exists():
            raise ValueError(f"output file already exists; refusing to overwrite: {target}")
    try:
        archive = zipfile.ZipFile(epub_path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise ValueError(f"cannot open EPUB ZIP archive: {exc}") from exc
    with archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("EPUB contains duplicate archive paths")
        if any(not _safe_archive_name(name) for name in names):
            raise ValueError("EPUB contains an unsafe archive path")
        if any(info.flag_bits & 0x1 for info in archive.infolist()):
            raise ValueError("encrypted EPUB ZIP entries are unsupported")
        if "mimetype" not in names or archive.read("mimetype") != b"application/epub+zip":
            raise ValueError("invalid EPUB: missing or incorrect mimetype entry")
        if "META-INF/encryption.xml" in names:
            raise ValueError("encrypted or DRM-protected EPUB content is unsupported")
        if "META-INF/container.xml" not in names:
            raise ValueError("invalid EPUB: missing META-INF/container.xml")
        container = _parse_document(archive.read("META-INF/container.xml"), "container.xml")
        rootfile = container.find(f".//{{{CONTAINER_NS}}}rootfile")
        if rootfile is None or not rootfile.get("full-path"):
            raise ValueError("invalid EPUB: container has no package document")
        package_path = rootfile.get("full-path", "")
        if not _safe_archive_name(package_path) or package_path not in names:
            raise ValueError(f"invalid or missing package document path: {package_path}")
        package = _parse_document(archive.read(package_path), package_path)
        metadata = package.find(f"{{{OPF_NS}}}metadata")
        if metadata is None:
            raise ValueError("invalid EPUB: package metadata is missing")
        title = metadata.findtext(f"{{{DC_NS}}}title")
        if not title or not title.strip():
            raise ValueError("invalid EPUB: required book title metadata is missing")
        manifest_node = package.find(f"{{{OPF_NS}}}manifest")
        spine_node = package.find(f"{{{OPF_NS}}}spine")
        if manifest_node is None or spine_node is None:
            raise ValueError("invalid EPUB: package manifest or spine is missing")
        manifest: dict[str, tuple[str, str]] = {}
        for item in manifest_node.findall(f"{{{OPF_NS}}}item"):
            item_id, href = item.get("id"), item.get("href")
            if not item_id or not href or item_id in manifest:
                raise ValueError("invalid EPUB: manifest item has missing or duplicate id/href")
            manifest[item_id] = (href, item.get("media-type", ""))
        refs = spine_node.findall(f"{{{OPF_NS}}}itemref")
        if not refs:
            raise ValueError("invalid EPUB: spine is empty")
        entries: list[dict[str, object]] = []
        warnings: list[str] = []
        if len(refs) > 1:
            warnings.append("spine documents do not necessarily map one-to-one to chapters; chapter boundaries spanning documents cannot be determined automatically")
        for ref in refs:
            item_id = ref.get("idref", "")
            if item_id not in manifest:
                raise ValueError(f"invalid EPUB: spine references unknown manifest id {item_id!r}")
            href, media_type = manifest[item_id]
            if media_type not in {"application/xhtml+xml", "text/html", "application/xml", "text/xml"}:
                raise ValueError(f"unsupported spine media type {media_type!r} for {href}")
            content_path = _resolve_href(package_path, href)
            if content_path not in names:
                raise ValueError(f"missing spine document: {content_path}")
            markdown, has_heading, heading_count, item_warnings = _html_to_markdown(
                archive.read(content_path), content_path,
                strict_xml=media_type in {"application/xhtml+xml", "application/xml", "text/xml"})
            if not markdown:
                warnings.append(f"{content_path}: no extractable text; skipped")
                continue
            if not has_heading:
                item_warnings.append("no heading found; document boundary used as an output chapter boundary")
            if heading_count > 1:
                item_warnings.append("multiple headings found; possible multiple chapters in one spine document; no boundary was inferred")
            output_name = output_path.name
            entries.append({"id": item_id, "href": href, "archive_path": content_path,
                            "output": output_name, "markdown": markdown,
                            "warnings": sorted(set(item_warnings))})
            warnings.extend(f"{output_name}: {warning}" for warning in item_warnings)

    manifest_data = {
        "source_epub": epub_path.name,
        "title": title.strip(),
        "reading_order": [{k: entry[k] for k in ("id", "href", "archive_path", "output", "warnings")} for entry in entries],
        "warnings": warnings,
    }
    if not entries:
        raise ValueError("EPUB contains no extractable text in its spine documents")
    manifest_data["output_file"] = str(output_path)
    manifest_data["manifest_file"] = str(manifest_path)
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = "\n".join(str(entry["markdown"]).rstrip() for entry in entries) + "\n"
    created: list[Path] = []
    try:
        with output_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(markdown)
        created.append(output_path)
        with manifest_path.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(manifest_data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        created.append(manifest_path)
    except OSError as exc:
        for path in created:
            path.unlink(missing_ok=True)
        raise ValueError(f"cannot write output files: {exc}") from exc
    return manifest_data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert an EPUB spine to ordered UTF-8 Markdown chapter files.")
    parser.add_argument("epub", type=Path, help="source .epub file")
    parser.add_argument("--output-dir", type=Path, help="destination directory (default: beside the EPUB)")
    args = parser.parse_args(argv)
    try:
        result = convert_epub(args.epub, args.output_dir)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Extracted {len(result['reading_order'])} spine documents to {result['output_file']}")
    for warning in result["warnings"]:
        print(f"Warning: {warning}", file=sys.stderr)
    print(f"Manifest: {result['manifest_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
