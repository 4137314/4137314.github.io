"""Dependency-free checks for the two maintained portfolio pages."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (ROOT / "index.html", ROOT / "portfolio/index.html")


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.text = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class SiteTests(unittest.TestCase):
    def test_page_landmarks_and_unique_ids(self):
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                doc = Document(page)
                ids = [a["id"] for _, a in doc.elements if "id" in a]
                self.assertEqual(len(ids), len(set(ids)))
                for tag in ("h1", "main", "title"):
                    self.assertEqual(sum(t == tag for t, _ in doc.elements), 1)
                self.assertTrue(any(t == "html" and a.get("lang") == "en" for t, a in doc.elements))
                self.assertTrue(any(t == "meta" and a.get("name") == "viewport" for t, a in doc.elements))
                self.assertTrue(any(t == "a" and a.get("class") == "skip-link" and a.get("href") == "#main" for t, a in doc.elements))
                for _, attrs in doc.elements:
                    if "aria-labelledby" in attrs:
                        for label in attrs["aria-labelledby"].split():
                            self.assertIn(label, ids)

    def test_local_links_assets_and_fragments_exist(self):
        for page in PAGES:
            doc = Document(page)
            for tag, attrs in doc.elements:
                for key in ("href", "src"):
                    if key not in attrs:
                        continue
                    with self.subTest(page=page.relative_to(ROOT), url=attrs[key]):
                        url = urlsplit(attrs[key])
                        if url.scheme or url.netloc:
                            continue
                        target = (ROOT / unquote(url.path).lstrip("/") if url.path.startswith("/")
                                  else page.parent / unquote(url.path)) if url.path else page
                        if target.is_dir():
                            target /= "index.html"
                        self.assertTrue(target.is_file(), f"Missing local target: {target}")
                        if url.fragment and target.suffix == ".html":
                            ids = {a.get("id") for _, a in Document(target).elements}
                            self.assertIn(unquote(url.fragment), ids)

    def test_external_links_use_secure_protocols(self):
        for page in PAGES:
            for tag, attrs in Document(page).elements:
                if tag == "a":
                    self.assertIn(urlsplit(attrs.get("href", "")).scheme, ("", "https", "mailto"))
                    if attrs.get("target") == "_blank":
                        self.assertIn("noopener", attrs.get("rel", "").split())

    def test_profile_and_private_document_boundaries(self):
        home = " ".join(Document(PAGES[0]).text).lower()
        self.assertIn("bachelor’s degree · in progress", home)
        self.assertIn("selected completed coursework", home)
        self.assertIn("ongoing training", home)
        self.assertIn("independent", home)
        for page in PAGES:
            source = page.read_text(encoding="utf-8").lower()
            for forbidden in ("piano_carriera", "matricola", "[your", "master's degree"):
                self.assertNotIn(forbidden, source)
            self.assertFalse(any(tag == "script" for tag, _ in Document(page).elements))

    def test_images_have_accessible_descriptions_and_reserved_space(self):
        for page in PAGES:
            for tag, attrs in Document(page).elements:
                if tag == "img":
                    with self.subTest(page=page.name, image=attrs.get("src")):
                        self.assertTrue(attrs.get("alt", "").strip())
                        self.assertGreater(int(attrs.get("width", 0)), 0)
                        self.assertGreater(int(attrs.get("height", 0)), 0)

    def test_home_links_to_selected_project_briefs(self):
        links = {attrs.get("href") for tag, attrs in Document(PAGES[0]).elements if tag == "a"}
        for project in ("risc-v", "ppse-firmware", "ald-cgra", "nixos-config",
                        "nixos-fleet", "ansible-baseline", "observability-stack", "ops-toolkit"):
            self.assertIn(f"projects/{project}/", links)

    def test_generated_portfolio_markers_remain_intact(self):
        source = PAGES[1].read_text(encoding="utf-8")
        for marker in ("<!-- GENERATED PROJECT INDEX START -->", "<!-- GENERATED PROJECT INDEX END -->"):
            self.assertEqual(source.count(marker), 1)
        self.assertLess(source.index("<!-- GENERATED PROJECT INDEX START -->"), source.index("<!-- GENERATED PROJECT INDEX END -->"))


if __name__ == "__main__":
    unittest.main()
