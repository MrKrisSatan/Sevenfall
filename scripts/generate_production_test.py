"""Nine-faction paid-production diagnostic; uses the harvesting map's resource fields."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]

def main():
    source = ROOT / 'mods/sevenfall/maps/release-test'
    dest = ROOT / 'mods/sevenfall/maps/production-test'
    dest.mkdir(exist_ok=True)
    text = (source / 'map.yaml').read_text()
    text = text.replace('Release Diagnostic', 'Production Diagnostic').replace('release-test.lua', 'production-test.lua')
    text = re.sub(r'\t(?:Power|Refinery)\d:.*?\n\t\tLocation:.*?\n', '', text, flags=re.S)
    (dest / 'map.yaml').write_text(text)
    (dest / 'map.bin').write_bytes((source / 'map.bin').read_bytes())

if __name__ == '__main__':
    main()
