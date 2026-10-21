# Website field guide

The [published catalogue](https://mrkrissatan.github.io/Sevenfall/forces.html)
covers all 63 current faction designs: 39 buildings and 24 units. Each faction
has 13 buildings, an MCV, a collector and six combat units. Three of those combat
units are subfaction exclusives. Selecting a subfaction includes its shared roster.

Building illustrations reuse the original high-resolution source art. MCVs and
collectors show one facing from the original high-resolution turnaround sheets.
The 18 combat-unit illustrations in `source/website/` are new concepts generated
with OpenAI image generation on 21 October 2026. They are clearly labelled in
the catalogue and **are not installed as game sprites**. No Red Alert artwork
is exported to the website. Air, naval and kennel unit rosters remain future work.

Exact prompts are in `website-unit-prompts.json`; source hashes are in
`website-unit-sources.json`. No reference images were supplied. Original-content
licensing remains as described in the repository; this pass assigns no new licence.

## Updating the catalogue

Names, descriptions and faction restrictions come from current MiniYaml rules
and Fluent strings. Yard and MCV entries are explicit because these actors share
their rules across factions. Update the generator for new artwork conventions or
new roster files. Edit `docs/catalogue.template.html`, not generated `forces.html`.

```sh
python scripts/build_site_catalogue.py
npm install
npm run site:art
python -m unittest discover -s tests
python -m http.server 8765 --directory docs
```

Sharp performs only cropping, trimming and resizing. Cards use 512×384 WebP;
the image viewer loads 1024×768 WebP on demand. Transparency is retained.
The catalogue is static HTML and works without JavaScript; JS adds filters,
shareable query URLs and the accessible image dialog. GitHub Pages publishes
the committed `docs/` folder from `main` through `.github/workflows/pages.yml`;
no server-side dependencies are needed. The workflow scopes `pages: write` and
`id-token: write` to the deployment job, as required by GitHub Pages.
