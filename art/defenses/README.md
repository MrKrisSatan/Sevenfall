# Original faction defense art

Fifteen defenses, five per faction, generated with built-in OpenAI image generation. `catalogue.json` records the design, prompts and style references. `source/` preserves the original outputs; `sheets/` contains technically packed six-frame atlases. No Red Alert artwork is included here.

Run `npm run art:defenses` to repack sources, export game sprites and icons, and update web images. Packing only extracts, scales and aligns the authored frames; it does not invent damage artwork. `manifest.json` records source/export SHA-256 hashes and individual frame hashes. Run `python scripts/build_defenses.py` to regenerate rules, sequences, weapons and localization.

Frames: healthy, damaged, critical, then three firing/pulse states. Dawn Wall uses frame 3 for its offline state. Small obstacles use 48-pixel frames; emplacements use 96-pixel frames. The runtime has damage variants and weapon firing sequences. Full gameplay and counters are documented in `docs/DEFENSES.md`.

Original-content licensing remains under review, consistent with the rest of the project's artwork.
