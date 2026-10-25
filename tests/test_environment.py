import importlib.util
from collections import deque
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('crossing', ROOT / 'scripts/generate_ashen_crossing.py')
crossing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crossing)


class CrossingTests(unittest.TestCase):
    def route(self, bridges):
        tiles, actors, _ = crossing.layout()
        blocked = set()
        for _, kind, x, y in actors:
            if kind.startswith('sf_') and 'bridge_ew' not in kind:
                size = 2 if kind in ('sf_cottage', 'sf_townhouse') else 1
                blocked.update((x+dx, y+dy) for dx in range(size) for dy in range(size))
        open_bridge = {(x, y) for y in bridges for x in range(62, 65)}
        queue, seen = deque([(18, 64)]), {(18, 64)}
        while queue:
            p = queue.popleft()
            if p == (108, 64):
                return True
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (p[0]+dx, p[1]+dy)
                if q in seen or q in blocked or not (1 <= q[0] <= 126 and 1 <= q[1] <= 126):
                    continue
                if tiles[q][0] in (1, 112, 113) and q not in open_bridge:
                    continue
                seen.add(q)
                queue.append(q)
        return False

    def test_either_intact_bridge_connects_banks(self):
        self.assertTrue(self.route([34]))
        self.assertTrue(self.route([92]))

    def test_destroyed_bridges_separate_banks(self):
        self.assertFalse(self.route([]))

    def test_resources_balanced_and_off_obstacles(self):
        tiles, actors, resources = crossing.layout()
        self.assertEqual(sum(v[1] for (x, y), v in resources.items() if x < 62),
                         sum(v[1] for (x, y), v in resources.items() if x > 64))
        for cell in resources:
            self.assertNotIn(tiles[cell][0], (1, 112, 113))
            self.assertNotIn(cell, [(x, y) for _, _, x, y in actors])

    def test_bridge_footprints_have_water_underneath(self):
        tiles, actors, _ = crossing.layout()
        for _, kind, x, y in actors:
            if kind == 'sf_bridge_ew':
                self.assertTrue(all(tiles[x+dx, y][0] == 1 for dx in range(3)))


if __name__ == '__main__':
    unittest.main()
