/* ==========================================================================
   microtools365 — shared site behavior
   ========================================================================== */

// Apply saved dark mode preference as early as possible (before
// DOMContentLoaded) to minimize the flash of light mode on load.
(function () {
  try {
    if (localStorage.getItem('mt365-theme') === 'dark') {
      document.documentElement.classList.add('dark-mode');
    }
  } catch (e) { /* localStorage unavailable — silently default to light */ }
})();

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
      document.body.classList.toggle('nav-locked', nav.classList.contains('open'));
    });
  }

  document.querySelectorAll('#year').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  // Homepage live search — filters .tool-card elements by data-keywords
  const searchInput = document.querySelector('#tool-search');
  if (searchInput) {
    const cards = Array.from(document.querySelectorAll('.tool-card'));
    const emptyState = document.querySelector('.empty-state');

    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;

      cards.forEach(card => {
        const haystack = (card.dataset.keywords || '') + ' ' + card.textContent.toLowerCase();
        const match = haystack.toLowerCase().includes(q);
        card.style.display = match ? '' : 'none';
        if (match) visibleCount++;
      });

      if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
      }
    });
  }

  // ---------- Dark mode toggle ----------
  // Injected into every page's header automatically, right before the
  // mobile hamburger button, so no individual page HTML needs editing.
  const headerContainer = document.querySelector('.site-header .container');
  const navToggleBtn = document.querySelector('.nav-toggle');
  if (headerContainer && navToggleBtn && !document.querySelector('.theme-toggle')) {
    const themeBtn = document.createElement('button');
    themeBtn.className = 'theme-toggle';
    themeBtn.setAttribute('aria-label', 'Toggle dark mode');
    themeBtn.textContent = document.documentElement.classList.contains('dark-mode') ? '☀️' : '🌙';
    headerContainer.insertBefore(themeBtn, navToggleBtn);

    themeBtn.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark-mode');
      themeBtn.textContent = isDark ? '☀️' : '🌙';
      try { localStorage.setItem('mt365-theme', isDark ? 'dark' : 'light'); }
      catch (e) { /* localStorage unavailable — theme won't persist, but toggle still works */ }
    });
  }
});

// Category dropdown menus in the header nav
document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.nav-dropdown-toggle');

  toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const menu = toggle.nextElementSibling;
      const isOpen = menu.classList.contains('open');

      document.querySelectorAll('.nav-dropdown-menu.open').forEach(m => m.classList.remove('open'));
      document.querySelectorAll('.nav-dropdown-toggle.open').forEach(t => t.classList.remove('open'));

      if (!isOpen) {
        menu.classList.add('open');
        toggle.classList.add('open');
      }
    });
  });

  document.addEventListener('click', () => {
    document.querySelectorAll('.nav-dropdown-menu.open').forEach(m => m.classList.remove('open'));
    document.querySelectorAll('.nav-dropdown-toggle.open').forEach(t => t.classList.remove('open'));
  });
});

// Small reusable toast notification — call showToast("Copied!")
function showToast(message) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), 1800);
}
