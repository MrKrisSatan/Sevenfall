# Sevenfall website

This is a static site designed for GitHub Pages.

## Enable publishing
The `.github/workflows/pages.yml` workflow publishes `docs/` when website files change on `main`. Repository owner: Settings → Pages → Build and deployment → Source: GitHub Actions. The workflow can also be started manually from Actions.

URL: https://mrkrissatan.github.io/Sevenfall/

The site's living issue list and release history use the public GitHub REST API in `site.js`; they update when GitHub Issues and Releases change. Static fallback text remains readable offline. No API tokens are embedded.

Page publication requires GitHub Pages to be enabled by the repository owner.