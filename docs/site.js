/* Public, read-only GitHub API. Site has static fallbacks if fetch is blocked. */
const repo = "MrKrisSatan/Sevenfall";
const root = "https://api.github.com/repos/" + repo;
const safe = value => String(value ?? "").replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
async function getJSON(path) {
  const response = await fetch(root + path, {headers: {"Accept": "application/vnd.github+json"}});
  if (!response.ok) throw new Error("GitHub unavailable: " + response.status);
  return response.json();
}
async function loadIssues() {
  const box = document.getElementById("issues");
  try {
    const all = await getJSON("/issues?state=open&per_page=100");
    const issues = all.filter(item => !item.pull_request).slice(0, 8);
    if (!issues.length) {box.innerHTML = '<p class="muted">No open issues yet. See the full roadmap for planned work.</p>'; return;}
    box.innerHTML = issues.map(item => '<div class="issue"><a href="' + safe(item.html_url) + '" target="_blank" rel="noopener">' + safe(item.title) + '</a><small>#' + safe(item.number) + '</small></div>').join("");
  } catch (error) {
    box.innerHTML = '<p class="muted">Tasks are available on <a href="https://github.com/MrKrisSatan/Sevenfall/issues">GitHub Issues ↗</a>.</p>';
  }
}
async function loadReleases() {
  const box = document.getElementById("releases-list");
  try {
    const list = await getJSON("/releases?per_page=5");
    if (!Array.isArray(list) || !list.length) return;
    box.innerHTML = list.map(release => {
      const published = release.published_at ? new Date(release.published_at).toLocaleDateString("en-GB", {year:"numeric",month:"short",day:"numeric"}) : "Unpublished";
      return '<div class="release-entry"><strong><a href="' + safe(release.html_url) + '" target="_blank" rel="noopener">' + safe(release.name || release.tag_name) + ' ↗</a></strong><p>' + safe(release.prerelease ? "Pre-release" : "Release") + ' · ' + safe(published) + ' · ' + safe(release.assets?.length || 0) + ' downloadable asset(s). Read release notes for testing status.</p></div>';
    }).join("");
  } catch (error) { /* Preserve visible no-build fallback */ }
}
loadIssues();
loadReleases();