"""Catch roster omissions, stale exports and broken published artwork."""
import collections
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalogue', ROOT / 'scripts/build_site_catalogue.py')
catalogue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalogue)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.images = []
        self.ids = []
        self.full_art = []
        self.options = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'img' and 'src' in a:
            self.images.append(a)
        if 'data-art' in a:
            self.full_art.append(a['data-art'])
        if tag == 'option':
            self.options.append(a.get('value'))


class WebsiteTests(unittest.TestCase):
    def test_complete_current_roster(self):
        records = catalogue.build_records()
        actual = json.loads((ROOT / 'docs/roster.json').read_text(encoding='utf-8'))
        self.assertEqual(actual, records, 'Run scripts/build_site_catalogue.py')
        ids = [r['id'] for r in records]
        self.assertEqual(len(ids), len(set(ids)))
        actors = set()
        for filename in ['20-structures.yaml', '25-support-structures.yaml', '30-units.yaml', '45-defenses.yaml','55-subfactions.yaml','60-identities.yaml']:
            actors.update(re.findall(r'^([A-Z][A-Z0-9_]+):', (ROOT / 'mods/sevenfall/rules' / filename).read_text(encoding='utf-8'), re.M))
        self.assertEqual({r['actor'] for r in records}, actors | {'FACT', 'MCV'})
        for faction in ['angels', 'humans', 'demons']:
            self.assertEqual(collections.Counter(r['kind'] for r in records if r['faction'] == faction), {'buildings': 23, 'units': 13})
        for sub in catalogue.SUBFACTIONS:
            self.assertEqual(sum(r['subfaction'] == sub for r in records), 4 if sub in ['a_desolation','h_area52','d_contempt'] else 3)
        for r in records:
            self.assertTrue(r['name'] and r['description'] and r['role'])
            self.assertTrue((ROOT / r['source']).is_file(), r['source'])

    def test_pages_and_artwork(self):
        for name in ['index.html', 'forces.html']:
            text = (ROOT / 'docs' / name).read_text(encoding='utf-8')
            for corrupt in ['\ufffd', '\u00e2\u20ac', '\u00c2\u00b7']:
                self.assertNotIn(corrupt, text)
            page = Page(text)
            self.assertEqual(len(page.ids), len(set(page.ids)))
            for image in page.images:
                self.assertTrue(image.get('alt'), image)
            for src in [i['src'] for i in page.images] + page.full_art:
                data = (ROOT / 'docs' / src).read_bytes()
                self.assertEqual(data[:4], b'RIFF', src)
                self.assertEqual(data[8:12], b'WEBP', src)
            if name == 'forces.html':
                for option in ['buildings', 'units', *catalogue.SUBFACTIONS]:
                    self.assertIn(option, page.options)
                self.assertEqual(len(page.images), 108)
                self.assertEqual(len(page.full_art), 108)
                expected = (ROOT / 'docs/catalogue.template.html').read_text(encoding='utf-8').replace('<!-- ROSTER_CARDS -->', '\n'.join(map(catalogue.render_card, catalogue.build_records())))
                self.assertEqual(text, expected)

    def test_concept_provenance(self):
        sources = json.loads((ROOT / 'art/website-unit-sources.json').read_text(encoding='utf-8'))
        prompts = json.loads((ROOT / 'art/website-unit-prompts.json').read_text(encoding='utf-8'))
        concepts = {r['id'] for r in catalogue.build_records() if r['status'] == 'Concept illustration'}
        self.assertEqual({r['id'] for r in sources['assets']}, concepts)
        self.assertEqual({r['id'] for r in prompts}, concepts)
        for r in sources['assets']:
            self.assertEqual(hashlib.sha256((ROOT / r['source']).read_bytes()).hexdigest(), r['sha256'])


if __name__ == '__main__':
    unittest.main()
