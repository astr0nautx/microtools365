/* ==========================================================================
   microtools365 — shared site behavior
   Things every page needs: mobile nav toggle, the current year in the
   footer, and a tiny toast helper. Tool-specific logic lives inside each
   tool's own page so every tool stays a self-contained, copyable example.
   ========================================================================== */

// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
  }

  // Auto-fill the footer year wherever #year exists
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
