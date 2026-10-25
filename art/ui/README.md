# Sevenfall interface themes

Original vector artwork authored in `scripts/build_ui.cjs`, GPL-3.0-or-later.
Run with Node and sharp to reproduce the SVG sources, 1x/2x/3x PNG atlases and
`mods/sevenfall/chrome-ui.yaml`. The preview is a palette/symbol reference,
not an in-game screenshot.

- Neutral: charcoal and silver; seven-sided geometric Sevenfall mark.
- Angelic: dark stone, ivory/gold trim and wing geometry.
- Human: blue-grey steel, teal trim and a fortified shield.
- Infernal: obsidian, ember trim and angular horn/crystal geometry.

All nine subfactions map to their parent theme through ChromeMetrics.
OpenRA's AddFactionSuffixLogic reads the actual local player's faction at HUD
creation, including resolved Random selections and campaign players. The
upstream GPL player layout is staged with faction binding added to the command
bar. It retains existing controls, hotkeys, dimensions and tooltips. Spectator
panels, menus, lobby, settings, loading brand and shellmap remain neutral.

This replaces panel skins and branding, not every functional glyph in the
inherited interface. Existing faction flags remain appropriate in faction/player
selectors. Generic OpenRA glyphs/layouts still require the ongoing dependency
and licence audit. Title text now uses the common FreeSans Bold font.

`--sf-check-chrome` validates the actual merged engine chrome and bounds of all
new image regions at three densities. Native launch, all-faction HUD switching,
small-window readability, button states and return-to-menu acceptance are still
pending; source validation is not an in-game visual pass.
