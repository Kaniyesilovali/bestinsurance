/* Minimum vanilla JS. İçerik HTML'in içinde — bu dosya yalnızca etkileşim ekler,
   hiçbir metni enjekte etmez. JS kapalıyken de sayfa eksiksiz okunur. */
(function () {
  'use strict';

  /* Mobil menü */
  var toggle = document.querySelector('[data-menu-toggle]');
  var menu = document.querySelector('[data-menu]');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.hasAttribute('hidden');
      if (open) { menu.removeAttribute('hidden'); } else { menu.setAttribute('hidden', ''); }
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  /* Kaydırınca beliren bölümler. Sayfadaki tek hareket kalıbı: 12px yükselme.
     Hareket azaltılmışsa hiç bağlanmıyoruz; CSS zaten her şeyi görünür bırakır. */
  var reveals = document.querySelectorAll('.reveal');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reveals.length && !still && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
    Array.prototype.forEach.call(reveals, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-in'); });
  }

  /* Şirket tablosu: arama + branşa göre filtre + sütuna göre sıralama.
     Tabloyu HTML'de hazır bulur, satırları yeniden yazmaz. */
  var table = document.querySelector('[data-filter-table]');
  if (!table) return;

  var tbody = table.tBodies[0];
  var rows = Array.prototype.slice.call(tbody.rows);
  var search = document.querySelector('[data-filter-search]');
  var branch = document.querySelector('[data-filter-branch]');
  var count = document.querySelector('[data-filter-count]');

  function apply() {
    var q = (search && search.value || '').toLocaleLowerCase('tr');
    var b = branch && branch.value || '';
    var shown = 0;
    rows.forEach(function (row) {
      var name = (row.dataset.name || '').toLocaleLowerCase('tr');
      var city = (row.dataset.city || '').toLocaleLowerCase('tr');
      var branches = row.dataset.branches || '';
      var ok = (!q || name.indexOf(q) > -1 || city.indexOf(q) > -1) &&
               (!b || branches.split(' ').indexOf(b) > -1);
      row.hidden = !ok;
      if (ok) shown++;
    });
    if (count) count.textContent = String(shown);
  }

  if (search) search.addEventListener('input', apply);
  if (branch) branch.addEventListener('change', apply);

  Array.prototype.forEach.call(table.querySelectorAll('[data-sort]'), function (th) {
    th.addEventListener('click', function () {
      var key = th.dataset.sort;
      var desc = th.dataset.dir !== 'desc';
      rows.sort(function (a, b) {
        var av = a.dataset[key] || '', bv = b.dataset[key] || '';
        var an = parseFloat(av), bn = parseFloat(bv);
        var cmp = (!isNaN(an) && !isNaN(bn)) ? an - bn : av.localeCompare(bv, 'tr');
        return desc ? -cmp : cmp;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
      Array.prototype.forEach.call(table.querySelectorAll('[data-sort]'), function (o) {
        o.removeAttribute('data-dir'); o.setAttribute('aria-sort', 'none');
      });
      th.dataset.dir = desc ? 'desc' : 'asc';
      th.setAttribute('aria-sort', desc ? 'descending' : 'ascending');
    });
  });
})();
