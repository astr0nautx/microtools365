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

  // ---------- Shared navigation and footer ----------
  // Keep site-wide links in one place even though this is a static site.
  const navigationGroups = [
    ['Finance', [['percentage-calculator', 'Percentage Calculator'], ['gst-calculator', 'GST Calculator'], ['emi-calculator', 'EMI Calculator'], ['sip-calculator', 'SIP Calculator'], ['compound-interest-calculator', 'Compound Interest'], ['income-tax-calculator', 'Income Tax Calculator'], ['in-hand-salary-calculator', 'In-Hand Salary'], ['fd-calculator', 'FD Calculator'], ['hra-calculator', 'HRA Exemption'], ['simple-interest-calculator', 'Simple Interest'], ['discount-calculator', 'Discount Calculator']]],
    ['Text', [['word-counter', 'Word Counter'], ['case-converter', 'Case Converter'], ['text-diff-checker', 'Text Diff Checker'], ['lorem-ipsum-generator', 'Lorem Ipsum Generator'], ['slug-generator', 'Slug Generator'], ['json-formatter', 'JSON Formatter']]],
    ['Personal', [['age-calculator', 'Age Calculator'], ['bmi-calculator', 'BMI Calculator'], ['calorie-calculator', 'BMR & Calorie Calculator'], ['ideal-weight-calculator', 'Ideal Weight Calculator'], ['pregnancy-due-date-calculator', 'Pregnancy Due Date']]],
    ['Documents', [['image-to-pdf', 'Image to PDF'], ['text-to-pdf', 'Text to PDF'], ['xls-to-pdf', 'Excel to PDF'], ['image-editor', 'Image Editor'], ['pdf-merge', 'Merge PDF'], ['pdf-split', 'Split PDF'], ['rent-receipt-generator', 'Rent Receipt Generator']]],
    ['Generators', [['random-name-picker', 'Name Picker'], ['password-generator', 'Password Generator'], ['qr-code-generator', 'QR Code Generator'], ['tip-calculator', 'Tip Calculator']]]
  ];
  const sharedNav = document.querySelector('.site-header .nav');
  if (sharedNav) {
    sharedNav.innerHTML = [
      '<a href="/">All tools</a>',
      '<a href="/blog/">Blog</a>',
      ...navigationGroups.map(([label, tools]) => `<div class="nav-item"><button class="nav-dropdown-toggle">${label} <span class="caret">▾</span></button><div class="nav-dropdown-menu">${tools.map(([id, name]) => `<a href="/tools/${id}/">${name}</a>`).join('')}</div></div>`)
    ].join('');
    const logo = document.querySelector('.site-header .logo');
    if (logo) logo.setAttribute('href', '/');
  }
  document.querySelectorAll('.site-footer .footer-links').forEach(footerLinks => {
    footerLinks.innerHTML = '<a href="/about/">About</a><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-use/">Terms of Use</a><a href="/blog/">Blog</a>';
  });
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


  // ---------- Tool discovery ----------
  const toolGroups = {
    finance: [
      ['percentage-calculator', 'Percentage Calculator'],
      ['gst-calculator', 'GST Calculator'],
      ['emi-calculator', 'EMI Calculator'],
      ['sip-calculator', 'SIP Calculator'],
      ['compound-interest-calculator', 'Compound Interest Calculator'],
      ['income-tax-calculator', 'Income Tax Calculator'],
      ['in-hand-salary-calculator', 'In-Hand Salary Calculator'],
      ['fd-calculator', 'FD Calculator'],
      ['hra-calculator', 'HRA Exemption Calculator'],
      ['simple-interest-calculator', 'Simple Interest Calculator'],
      ['discount-calculator', 'Discount Calculator']
    ],
    text: [
      ['word-counter', 'Word Counter'],
      ['case-converter', 'Case Converter'],
      ['text-diff-checker', 'Text Diff Checker'],
      ['lorem-ipsum-generator', 'Lorem Ipsum Generator'],
      ['slug-generator', 'Slug Generator'],
      ['json-formatter', 'JSON Formatter']
    ],
    personal: [
      ['age-calculator', 'Age Calculator'],
      ['bmi-calculator', 'BMI Calculator'],
      ['calorie-calculator', 'Calorie Calculator'],
      ['ideal-weight-calculator', 'Ideal Weight Calculator'],
      ['pregnancy-due-date-calculator', 'Pregnancy Due Date Calculator']
    ],
    documents: [
      ['image-to-pdf', 'Image to PDF'],
      ['text-to-pdf', 'Text to PDF'],
      ['xls-to-pdf', 'Excel to PDF'],
      ['image-editor', 'Image Editor & Converter'],
      ['pdf-merge', 'Merge PDF'],
      ['pdf-split', 'Split PDF'],
      ['rent-receipt-generator', 'Rent Receipt Generator']
    ],
    generators: [
      ['random-name-picker', 'Random Name Picker'],
      ['password-generator', 'Password Generator'],
      ['qr-code-generator', 'QR Code Generator'],
      ['tip-calculator', 'Tip Calculator']
    ]
  };

  const currentTool = location.pathname.match(/\/tools\/([^/]+)\/?/);
  if (currentTool) {
    const slug = currentTool[1];
    const group = Object.values(toolGroups).find(tools => tools.some(([id]) => id === slug));

    try {
      const recent = JSON.parse(localStorage.getItem('mt365-recent-tools') || '[]')
        .filter(id => id !== slug && Object.values(toolGroups).flat().some(([known]) => known === id));
      recent.unshift(slug);
      localStorage.setItem('mt365-recent-tools', JSON.stringify(recent.slice(0, 4)));
    } catch (e) { /* recent tools are optional */ }

    if (group) {
      const related = group.filter(([id]) => id !== slug).slice(0, 3);
      if (related.length && !document.querySelector('.related-tools')) {
        const section = document.createElement('section');
        section.className = 'section related-tools';
        section.innerHTML = `<div class="container"><h2 class="section-title">Related tools</h2><div class="related-tools-list">${related.map(([id, name]) => `<a href="/tools/${id}/">${name}<span aria-hidden="true">→</span></a>`).join('')}</div></div>`;
        const footer = document.querySelector('.site-footer');
        if (footer) footer.parentNode.insertBefore(section, footer);
      }
    }
  }

  const onHomePage = location.pathname === '/' || /\/index\.html$/.test(location.pathname);
  if (onHomePage && !document.querySelector('.recent-tools')) {
    try {
      const ids = JSON.parse(localStorage.getItem('mt365-recent-tools') || '[]');
      const allTools = Object.values(toolGroups).flat();
      const recent = ids.map(id => allTools.find(([known]) => known === id)).filter(Boolean);
      if (recent.length) {
        const section = document.createElement('section');
        section.className = 'section recent-tools';
        section.innerHTML = `<div class="container"><h2 class="section-title">Recently used</h2><div class="related-tools-list">${recent.map(([id, name]) => `<a href="/tools/${id}/">${name}<span aria-hidden="true">→</span></a>`).join('')}</div></div>`;
        const hero = document.querySelector('.hero');
        if (hero) hero.insertAdjacentElement('afterend', section);
      }
    } catch (e) { /* recent tools are optional */ }
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
