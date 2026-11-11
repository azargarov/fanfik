import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from markdown_to_epub import build_epub


class MarkdownToEpubTest(unittest.TestCase):
    def test_builds_ordered_epub3_and_formats_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "chapter1.md"
            second = root / "chapter2.md"
            first.write_text("# First\n\nOne paragraph with **bold** and *italic*.\n\nSecond paragraph.\n", encoding="utf-8")
            second.write_text("# Second\n\n- item one\n- item two\n", encoding="utf-8")
            output = build_epub([first, second], root / "sample.epub", title="Synthetic Book", author="Test Author")
            with zipfile.ZipFile(output) as epub:
                names = epub.namelist()
                self.assertEqual(names[0], "mimetype")
                self.assertEqual(epub.read("mimetype"), b"application/epub+zip")
                opf = ET.fromstring(epub.read("OEBPS/package.opf"))
                ns = {"opf":"http://www.idpf.org/2007/opf", "dc":"http://purl.org/dc/elements/1.1/"}
                self.assertEqual(opf.findtext("opf:metadata/dc:language", namespaces=ns), "ru")
                self.assertEqual([node.get("idref") for node in opf.findall("opf:spine/opf:itemref", ns)], ["c1", "c2"])
                nav = epub.read("OEBPS/nav.xhtml").decode()
                self.assertLess(nav.index("First"), nav.index("Second"))
                xhtml = epub.read("OEBPS/chapter001.xhtml").decode()
                self.assertIn("<strong>bold</strong>", xhtml)
                self.assertIn("<em>italic</em>", xhtml)
                self.assertEqual(xhtml.count("<p>"), 2)
                ET.fromstring(epub.read("OEBPS/chapter002.xhtml"))

    def test_missing_chapter_fails_clearly(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "does not exist"):
                build_epub([Path(temp) / "missing.md"], Path(temp) / "x.epub", title="X", author="Y")


if __name__ == "__main__":
    unittest.main()
