import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from epub_to_markdown import convert_epub


def make_epub(path: Path, *, content: dict[str, str] | None = None,
              spine: list[str] | None = None, package: str | None = None,
              extra: dict[str, bytes] | None = None) -> Path:
    if content is None:
        content = {"Text/z.xhtml": "<html xmlns='http://www.w3.org/1999/xhtml'><body><h1>One</h1><p>Hello <em>dear</em> <strong>reader</strong>.</p></body></html>",
                   "Text/a.xhtml": "<html xmlns='http://www.w3.org/1999/xhtml'><body><h1>Two</h1><p>Привет, мир.</p></body></html>"}
    items = [(Path(href).stem, href) for href in content]
    spine = spine if spine is not None else [item_id for item_id, _ in items]
    manifest_items = "".join(f'<item id="{item_id}" href="{href}" media-type="application/xhtml+xml" />'
                             for item_id, href in items)
    refs = "".join(f'<itemref idref="{item_id}" />' for item_id in spine)
    package = package or (f'<package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Fixture</dc:title><dc:language>en</dc:language></metadata><manifest>{manifest_items}</manifest><spine>{refs}</spine></package>')
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OPS/book.opf"/></rootfiles></container>')
        zf.writestr("OPS/book.opf", package)
        for name, text in content.items():
            zf.writestr("OPS/" + name, text)
        for name, data in (extra or {}).items():
            zf.writestr(name, data)
    return path


class EpubToMarkdownTest(unittest.TestCase):
    def test_spine_order_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); epub = make_epub(root / "book.epub")
            manifest = convert_epub(epub, root / "out")
            self.assertEqual([e["archive_path"] for e in manifest["reading_order"]], ["OPS/Text/z.xhtml", "OPS/Text/a.xhtml"])
            text = (root / "out/book.md").read_text(encoding="utf-8")
            self.assertIn("# One", text)
            self.assertIn("# Two", text)
            self.assertTrue((root / "out/manifest.json").is_file())
            self.assertEqual(json.loads((root / "out/manifest.json").read_text())["title"], "Fixture")

    def test_formatting_paragraphs_and_unicode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = {"Text/z.xhtml": "<html><body><h2>Chapter Ω</h2><p>First <i>italic</i> and <b>bold</b>.</p><p>Second — dialogue: “Hello!”</p><hr/><p>End.</p></body></html>"}
            make_epub(root / "book.epub", content=content, spine=["z"])
            convert_epub(root / "book.epub", root / "out")
            text = (root / "out/book.md").read_text(encoding="utf-8")
            self.assertIn("## Chapter Ω", text)
            self.assertIn("*italic*", text)
            self.assertIn("**bold**", text)
            self.assertIn("Second — dialogue: “Hello!”", text)
            self.assertGreaterEqual(text.count("\n\n"), 2)
            self.assertIn("---", text)

    def test_table_rows_and_cells_keep_text_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = {
                "Text/poem.xhtml": (
                    "<html><body><h1>Poem</h1><table>"
                    "<tr><td>Kansas,</td><td>And</td></tr>"
                    "<tr><td><i>When</i></td><td>marry…</td></tr>"
                    "</table><p>After.</p></body></html>"
                )
            }
            epub = make_epub(root / "book.epub", content=content)
            convert_epub(epub, root / "out")
            text = (root / "out/book.md").read_text(encoding="utf-8")
            self.assertIn("Kansas, And\n\n*When* marry…", text)
            self.assertIn("marry…\n\nAfter.", text)

    def test_missing_or_malformed_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            no_meta = '<package xmlns="http://www.idpf.org/2007/opf"><manifest/><spine/></package>'
            make_epub(root / "bad.epub", package=no_meta)
            with self.assertRaisesRegex(ValueError, "metadata"):
                convert_epub(root / "bad.epub", root / "out")
            make_epub(root / "bad2.epub", package="<package>")
            with self.assertRaisesRegex(ValueError, "malformed XML"):
                convert_epub(root / "bad2.epub", root / "out2")

    def test_encrypted_content_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); make_epub(root / "book.epub", extra={"META-INF/encryption.xml": b"<encryption/>"})
            with self.assertRaisesRegex(ValueError, "encrypted or DRM"):
                convert_epub(root / "book.epub", root / "out")

    def test_output_conflicts_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); epub = make_epub(root / "book.epub")
            existing_dir = root / "out"; existing_dir.mkdir()
            existing_file = existing_dir / "book.md"; existing_file.write_text("keep")
            with self.assertRaisesRegex(ValueError, "already exists"):
                convert_epub(epub, existing_dir)
            self.assertEqual(existing_file.read_text(), "keep")

    def test_default_output_is_single_markdown_beside_epub(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); epub = make_epub(root / "book.epub")
            result = convert_epub(epub)
            self.assertEqual(Path(result["output_file"]), root / "book.md")
            self.assertTrue((root / "book.md").is_file())
            self.assertTrue((root / "book.manifest.json").is_file())

    def test_empty_spine_document_is_skipped_in_reading_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = {
                "Text/cover.xhtml": "<html><body><img src='../cover.jpg' alt=''/></body></html>",
                "Text/first.xhtml": "<html><body><h1>First</h1><p>Text one.</p></body></html>",
                "Text/second.xhtml": "<html><body><h1>Second</h1><p>Text two.</p></body></html>",
            }
            epub = make_epub(root / "book.epub", content=content, spine=["cover", "first", "second"])
            result = convert_epub(epub, root / "out")
            text = (root / "out/book.md").read_text(encoding="utf-8")
            self.assertEqual([entry["id"] for entry in result["reading_order"]], ["first", "second"])
            self.assertLess(text.index("Text one."), text.index("Text two."))
            self.assertTrue(any("cover.xhtml" in warning and "skipped" in warning for warning in result["warnings"]))

    def test_entire_epub_without_extractable_text_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = {"Text/cover.xhtml": "<html><body><img src='../cover.jpg'/></body></html>"}
            epub = make_epub(root / "empty.epub", content=content, spine=["cover"])
            with self.assertRaisesRegex(ValueError, "no extractable text"):
                convert_epub(epub)
            self.assertFalse((root / "empty.md").exists())

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = ('<package xmlns="http://www.idpf.org/2007/opf"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Fixture</dc:title></metadata><manifest><item id="x" href="../../escape.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="x"/></spine></package>')
            make_epub(root / "book.epub", package=package)
            with self.assertRaisesRegex(ValueError, "escapes archive root"):
                convert_epub(root / "book.epub", root / "out")

    def test_multiple_chapters_in_one_document_are_not_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = {"Text/z.xhtml": "<html><body><h1>Chapter 1</h1><p>First.</p><h1>Chapter 2</h1><p>Second.</p></body></html>"}
            make_epub(root / "book.epub", content=content, spine=["z"])
            manifest = convert_epub(root / "book.epub", root / "out")
            self.assertEqual(len(manifest["reading_order"]), 1)
            self.assertTrue(any("possible multiple chapters" in warning for warning in manifest["warnings"]))
            text = (root / "out/book.md").read_text()
            self.assertEqual(text.count("# Chapter"), 2)

    def test_archive_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); epub = make_epub(root / "book.epub")
            with zipfile.ZipFile(epub, "a") as zf:
                zf.writestr("../outside", "x")
            with self.assertRaisesRegex(ValueError, "unsafe archive path"):
                convert_epub(epub, root / "out")


if __name__ == "__main__":
    unittest.main()
