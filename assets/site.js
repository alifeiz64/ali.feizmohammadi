(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  if (menu && nav) {
    const setMenu = (open) => {
      menu.setAttribute('aria-expanded', String(open));
      menu.textContent = open ? 'Close' : 'Menu';
      nav.classList.toggle('is-open', open);
    };
    menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (event) => { if (event.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        setMenu(false); menu.focus();
      }
    });
  }
  const search = document.querySelector('#paper-search');
  if (!search) return;
  document.querySelector('.publication-tools').hidden = false;
  const papers = [...document.querySelectorAll('.paper')];
  const buttons = [...document.querySelectorAll('.filter-button')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty-results');
  let status = 'all';
  const normalize = (text) => text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  const termsByPaper = new Map(papers.map(paper => [paper, normalize(paper.dataset.search)]));
  function applyFilters() {
    const words = normalize(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const paper of papers) {
      const match = (status === 'all' || paper.dataset.status === status) && words.every(word => termsByPaper.get(paper).includes(word));
      paper.hidden = !match;
      if (match) visible++;
    }
    document.querySelectorAll('.pub-year, .pub-section').forEach(group => {
      group.hidden = ![...group.querySelectorAll('.paper')].some(paper => !paper.hidden);
    });
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === status));
    count.textContent = `${visible} of ${papers.length} papers${words.length ? ' match your search' : ''}`;
    empty.hidden = visible !== 0;
    const url = new URL(window.location.href);
    if (status === 'all') url.searchParams.delete('type'); else url.searchParams.set('type', status);
    if (search.value.trim()) url.searchParams.set('q', search.value.trim()); else url.searchParams.delete('q');
    try { window.history.replaceState(null, '', url); } catch (_) { /* Local file previews still work. */ }
  }
  function readFilters() {
    const params = new URLSearchParams(window.location.search);
    const wanted = params.get('type');
    status = ['published', 'preprint', 'earlier'].includes(wanted) ? wanted : 'all';
    search.value = params.get('q') || '';
    applyFilters();
  }
  buttons.forEach(button => button.addEventListener('click', () => { status = button.dataset.filter; applyFilters(); }));
  search.addEventListener('input', applyFilters);
  document.querySelector('#reset-search').addEventListener('click', () => { status = 'all'; search.value = ''; applyFilters(); search.focus(); });
  window.addEventListener('popstate', readFilters);
  readFilters();
})();
