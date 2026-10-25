import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


TEST_FILE = Path(__file__).resolve()
REPOSITORY = TEST_FILE.parent.parent
OUTPUT = REPOSITORY / "public"


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.board = {}
        self.canonical = None
        source = path.read_text(encoding="utf-8")
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for name in ["href", "src"]:
            target = attributes.get(name)
            if target:
                self.links.append(target)
        if attributes.get("rel") == "canonical":
            self.canonical = attributes["href"]
        if attributes.get("id") == "knowledge-board":
            self.board = attributes


class BuiltSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        homepage = OUTPUT / "index.html"
        cls.home = Document(homepage)
        cls.origin = urlsplit(cls.home.canonical)

    def local_file(self, page, target):
        relative_page = page.relative_to(OUTPUT)
        page_url = urljoin(self.home.canonical, str(relative_page))
        target_url = urljoin(page_url, target)
        resolved = urlsplit(target_url)
        if resolved.scheme not in ["http", "https"]:
            return None
        if resolved.netloc != self.origin.netloc:
            return None
        path = unquote(resolved.path)
        within_site = path.startswith(self.origin.path)
        self.assertTrue(within_site, f"{page}: {target} escapes the site base path")
        relative = path[len(self.origin.path):]
        local = OUTPUT / relative
        if local.is_dir():
            local = local / "index.html"
        exists = local.is_file()
        self.assertTrue(exists, f"{page}: {target} has no built file at {local}")
        return local

    def test_internal_links_have_built_targets(self):
        for page in OUTPUT.rglob("*.html"):
            document = Document(page)
            for target in document.links:
                self.local_file(page, target)

    def test_maps_use_the_tagged_remote_renderer_and_local_notes(self):
        expected_renderer = (
            "https://cdn.jsdelivr.net/gh/drmingdrmer/"
            "obsidian-canvas-render@v0.1.0/canvas-render.js"
        )
        for page in OUTPUT.rglob("*.html"):
            document = Document(page)
            if not document.board:
                continue
            canvas = self.local_file(page, document.board["data-canvas"])
            renderer = document.board["data-renderer"]
            self.assertEqual(renderer, expected_renderer)
            source = canvas.read_text(encoding="utf-8")
            data = json.loads(source)
            for node in data.get("nodes", []):
                if node["type"] != "file":
                    continue
                target = document.board["data-vault"] + node["file"]
                self.local_file(page, target)

    def test_every_map_has_a_topic_page(self):
        actual = []
        for page in OUTPUT.rglob("*.html"):
            document = Document(page)
            if document.board:
                canvas = self.local_file(page, document.board["data-canvas"])
                actual.append(canvas)
        canvas_root = OUTPUT / "canvases"
        expected = list(canvas_root.rglob("*.canvas"))
        notes_root = OUTPUT / "vault/notes"
        expected.extend(notes_root.rglob("*.canvas"))
        self.assertCountEqual(actual, expected)

    def test_canvas_files_resolve_inside_the_obsidian_vault(self):
        vault = REPOSITORY / "vault"
        vault = vault.resolve()
        for canvas in vault.rglob("*.canvas"):
            relative = canvas.relative_to(vault)
            if relative.parts[0] not in {"canvases", "notes"}:
                continue
            source = canvas.read_text(encoding="utf-8")
            data = json.loads(source)
            for node in data.get("nodes", []):
                if node["type"] != "file":
                    continue
                target = vault / node["file"]
                target = target.resolve()
                within_vault = target.is_relative_to(vault)
                self.assertTrue(within_vault, str(canvas))
                exists = target.is_file()
                self.assertTrue(exists, f"{canvas}: {node['file']}")

    def test_vault_files_are_published_unchanged(self):
        vault = REPOSITORY / "vault"
        excluded = {".obsidian", ".trash", "pages", "plans"}
        for source in vault.rglob("*"):
            if not source.is_file():
                continue
            relative = source.relative_to(vault)
            if relative.parts[0] in excluded:
                continue
            if relative.parts[0] == "canvases":
                published = OUTPUT / relative
            else:
                published = OUTPUT / "vault" / relative
            actual = published.read_bytes()
            expected = source.read_bytes()
            self.assertEqual(actual, expected, str(relative))

    def test_earlier_note_urls_remain_available(self):
        notes = REPOSITORY / "vault/notes"
        for source in notes.rglob("*.md"):
            relative = source.relative_to(notes)
            published = OUTPUT / "vault" / relative
            actual = published.read_bytes()
            expected = source.read_bytes()
            self.assertEqual(actual, expected, str(relative))

    def test_vault_settings_and_authoring_sources_are_not_published(self):
        for directory in [".obsidian", ".trash", "pages", "plans"]:
            published = OUTPUT / "vault" / directory
            files = []
            for path in published.rglob("*"):
                if path.is_file():
                    files.append(str(path))
            self.assertEqual(files, [])


if __name__ == "__main__":
    unittest.main()
