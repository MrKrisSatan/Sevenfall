"""Source-level checks for the planned Sevenfall 75-mission narrative.

This does not execute any OpenRA campaign map or assert mission playability.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "design" / "CAMPAIGN_MISSIONS.md"
BIBLE = ROOT / "design" / "STORY_BIBLE.md"
PAGE = ROOT / "docs" / "campaigns.html"
EXPECTED_ORIGINAL_TITLES = {
    "H": (
        "The Day the Sky Broke", "Last Light", "The Glass Fields",
        "Do Not Look Up", "The Endless Descent", "The False Sanctuary",
        "Broken Covenant", "We Remain",
    ),
    "A": (
        "The Call to Arms", "The Choir Unbroken", "A Glass of Wrath",
        "The Emperor of Ash", "The Mortal Refusal", "The Unshackling",
        "The Empty Gate", "Judgment Deferred",
    ),
    "D": (
        "Hunger Wakes", "Seeds of Ruin", "The Gate Eaters",
        "Iron and Horn", "The Crown Below", "Blasphemous Engine",
        "The Court's Price", "The Shape of Freedom",
    ),
}


def get_missions(text):
    pattern = r"(?ms)^#### ([HAD])(\d{2})\. ([^\n]+)\n(.*?)(?=^#### [HAD]\d{2}\.|^### ACT |^## |\Z)"
    return [
        (side, int(number), title, body)
        for side, number, title, body in re.findall(pattern, text)
    ]


class MissionPageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.mission_ids = []
        self.image_sources = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                raise AssertionError("Duplicate HTML id " + a["id"])
            self.ids.add(a["id"])
        if tag == "details" and "mission" in a.get("class", "").split():
            self.mission_ids.append(a.get("id"))
        if tag == "img":
            self.image_sources.append((a.get("src"), a.get("alt")))


class CampaignDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = ATLAS.read_text(encoding="utf-8")
        cls.missions = get_missions(cls.atlas)

    def test_all_75_numbered_briefs_are_complete(self):
        self.assertEqual(len(self.missions), 75)
        for faction in "HAD":
            faction_missions = [
                (n, title, body) for f, n, title, body in self.missions if f == faction
            ]
            self.assertEqual([n for n, _, _ in faction_missions], list(range(1, 26)))
            self.assertEqual(len({title for _, title, _ in faction_missions}), 25)
            for number, title, body in faction_missions:
                with self.subTest(mission=f"{faction}{number:02} {title}"):
                    for key in ("Theatre", "Primary", "Failure", "Story"):
                        self.assertIn(f"**{key}:**", body)
                    self.assertIn("**Optional", body)

    def test_original_eight_titles_preserved_in_story_order(self):
        for faction, expected in EXPECTED_ORIGINAL_TITLES.items():
            titles = [t for f, _, t, _ in self.missions if f == faction]
            positions = [titles.index(title) for title in expected]
            self.assertEqual(positions, sorted(positions), faction)
            self.assertEqual(titles[-1], expected[-1])

    def test_five_acts_per_campaign_and_crossovers(self):
        self.assertEqual(len(re.findall(r"(?m)^### ACT [IVX]+:", self.atlas)), 15)
        for identifier in ("H07", "A08", "H10", "A10", "D12", "H25", "A25", "D25"):
            self.assertIn(identifier, self.atlas)
        self.assertIn("H25, A25 and D25 are mutually exclusive", self.atlas)

    def test_public_campaign_page_matches_mission_atlas(self):
        text = PAGE.read_text(encoding="utf-8")
        parser = MissionPageParser()
        parser.feed(text)
        expected = [f"{f.lower()}{number:02}" for f, number, _, _ in self.missions]
        self.assertEqual(parser.mission_ids, expected)
        self.assertEqual(len(parser.mission_ids), 75)
        for source, alt in parser.image_sources:
            self.assertTrue(source and alt)
            self.assertTrue((ROOT / "docs" / source).is_file(), source)

    def test_project_documents_use_new_scope(self):
        bible = BIBLE.read_text(encoding="utf-8")
        game_design = (ROOT / "design" / "GAME_DESIGN.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        home = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("75 missions", bible)
        self.assertIn("25 missions", game_design)
        self.assertIn("75 narrative missions", roadmap)
        self.assertIn('href="campaigns.html"', home)
        self.assertIn('href="campaigns.html"', (ROOT / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
