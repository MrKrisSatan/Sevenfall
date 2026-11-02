# Sevenfall interface themes

Original vector artwork authored in `scripts/build_ui.cjs`, GPL-3.0-or-later.
Run with Node and sharp to reproduce the SVG sources, 1x/2x/3x PNG atlases and
`mods/sevenfall/chrome-ui.yaml`. The preview is a palette/symbol reference,
not an in-game screenshot.

- Neutral: charcoal and silver; seven-sided geometric Sevenfall mark.
- Angelic: dark stone, ivory/gold trim and wing geometry.
- Human: blue-grey steel, teal trim and a fortified shield.
- Infernal: obsidian, ember trim and angular horn/crystal geometry.
- Machine: dark blue steel, cyan trim and geometric circuit imagery.
- Fallen: dark violet stone, pale lavender trim and broken celestial imagery.

- Veilborn: turquoise mineral facets and gold veins.
- Unwritten: silver memory ribbons and an archive mark.
- Outer Silence: violet void geometry on near-black panels.
- Nephilim: ochre stone and bronze oath geometry.

All twenty original subfactions and four independent faction IDs map to their parent theme through ChromeMetrics. Veilborn remains hidden in the normal lobby.
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
