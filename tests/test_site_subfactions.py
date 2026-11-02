"""Profiles must cover every selectable subfaction and link to real roster art."""
import sys
import unittest
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import build_site_subfactions as profiles

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.images=[]; self.ids=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a': self.links.append(attrs.get('href',''))
        if tag=='img': self.images.append(attrs['src'])
        if 'id' in attrs: self.ids.append(attrs['id'])

class SubfactionProfiles(unittest.TestCase):
    def test_current_profiles_and_home_links(self):
        root=profiles.ROOT/'docs'
        text=(root/'subfactions.html').read_text(encoding='utf-8')
        self.assertEqual(text, profiles.render())
        page=Links(text); home=Links((root/'index.html').read_text(encoding='utf-8'))
        self.assertEqual(len(profiles.TACTICS),20)
        self.assertEqual(len(page.images),40)
        for sid in profiles.TACTICS:
            self.assertIn(sid,page.ids)
            self.assertIn('subfactions.html#'+sid,home.links)
        for image in page.images:
            self.assertTrue((root/image).is_file(),image)
        for realm in ['machine','fallen']:
            self.assertIn('assets/roster/'+realm+'-emblem.webp',home.images)

if __name__=='__main__':unittest.main()
