/* All roster cards are static HTML. Filtering and artwork viewing are enhancements. */
(() => {
  const form = document.getElementById('roster-filters');
  const cards = [...document.querySelectorAll('.roster-card')];
  const buttons = [...document.querySelectorAll('[data-filter-faction]')];
  const search = document.getElementById('roster-search');
  const kind = document.getElementById('roster-kind');
  const subfaction = document.getElementById('roster-subfaction');
  const params = new URLSearchParams(location.search);
  let faction = ['angels','humans','demons'].includes(params.get('faction')) ? params.get('faction') : 'all';
  const parents = {a:'angels',h:'humans',d:'demons'};
  search.value = params.get('q') || '';
  kind.value = ['buildings','units'].includes(params.get('type')) ? params.get('type') : 'all';
  if ([...subfaction.options].some(o => o.value === params.get('subfaction'))) subfaction.value = params.get('subfaction');
  if (subfaction.value !== 'all') faction = parents[subfaction.value[0]];
  const entries = cards.map(card => ({card,text:card.textContent.toLowerCase()}));
  function applyFilters() {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    entries.forEach(({card,text}) => {
      const d = card.dataset;
      const visible = (faction === 'all' || d.faction === faction) &&
        (kind.value === 'all' || d.kind === kind.value) &&
        (subfaction.value === 'all' || d.subfaction === 'shared' || d.subfaction === subfaction.value) && text.includes(query);
      card.hidden = !visible;
      if (visible) count++;
    });
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filterFaction === faction)));
    [...subfaction.options].forEach(o => {o.disabled = o.value !== 'all' && faction !== 'all' && parents[o.value[0]] !== faction;});
    document.getElementById('roster-count').textContent = `${count} ${count === 1 ? 'entry' : 'entries'}${subfaction.value !== 'all' ? ' · includes shared faction roster' : ''}`;
    document.getElementById('roster-empty').hidden = count !== 0;
    const next = new URLSearchParams();
    if (faction !== 'all') next.set('faction',faction);
    if (kind.value !== 'all') next.set('type',kind.value);
    if (subfaction.value !== 'all') next.set('subfaction',subfaction.value);
    if (query) next.set('q',search.value.trim());
    history.replaceState(null,'',location.pathname+(next.size ? '?'+next.toString() : '')+location.hash);
  }
  buttons.forEach(b => b.addEventListener('click',() => {faction=b.dataset.filterFaction;subfaction.value='all';applyFilters();}));
  search.addEventListener('input',applyFilters);
  kind.addEventListener('change',applyFilters);
  subfaction.addEventListener('change',() => {if(subfaction.value!=='all') faction=parents[subfaction.value[0]];applyFilters();});
  form.addEventListener('submit',e => e.preventDefault());
  form.addEventListener('reset',e => {e.preventDefault();faction='all';search.value='';kind.value='all';subfaction.value='all';applyFilters();});
  form.hidden=false;
  applyFilters();
  const dialog = document.getElementById('art-dialog');
  let opener;
  document.querySelectorAll('.art-button').forEach(button => button.addEventListener('click',() => {
    const card = button.closest('.roster-card');
    const full = document.getElementById('art-full');
    full.src=button.dataset.art;full.alt=button.querySelector('img').alt;
    document.getElementById('art-title').textContent=card.querySelector('h3').textContent;
    document.getElementById('art-label').textContent=card.querySelector('.card-kicker').textContent+' / '+card.querySelector('.art-status span').textContent;
    document.getElementById('art-description').textContent=card.querySelector('.roster-card-copy>h3+p').textContent;
    document.getElementById('art-availability').textContent=card.querySelector('.availability').textContent;
    opener=button;dialog.showModal();
  }));
  dialog.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
  dialog.addEventListener('close',()=>opener?.focus());
})();
