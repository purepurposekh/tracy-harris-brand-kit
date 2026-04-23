// Navigation, hover + click for desktop dropdowns, burger drawer for mobile.
(function () {
  // --- Desktop dropdowns ---
  const items = document.querySelectorAll('.nav__item[data-has-panel="true"]');
  let openItem = null;
  let closeTimer = null;

  function openItemEl(item) {
    if (openItem && openItem !== item) {
      openItem.setAttribute('data-open', 'false');
      openItem.querySelector('.nav__trigger')?.setAttribute('aria-expanded', 'false');
    }
    item.setAttribute('data-open', 'true');
    item.querySelector('.nav__trigger')?.setAttribute('aria-expanded', 'true');
    openItem = item;
    clearTimeout(closeTimer);
  }

  function closeItemEl(item, delay) {
    closeTimer = setTimeout(() => {
      item.setAttribute('data-open', 'false');
      item.querySelector('.nav__trigger')?.setAttribute('aria-expanded', 'false');
      if (openItem === item) openItem = null;
    }, delay || 0);
  }

  items.forEach((item) => {
    const trigger = item.querySelector('.nav__trigger');
    item.addEventListener('mouseenter', () => openItemEl(item));
    item.addEventListener('mouseleave', () => closeItemEl(item, 120));
    trigger?.addEventListener('click', (e) => {
      e.preventDefault();
      const isOpen = item.getAttribute('data-open') === 'true';
      if (isOpen) closeItemEl(item, 0);
      else openItemEl(item);
    });
    trigger?.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeItemEl(item, 0);
        trigger.focus();
      }
    });
  });

  document.addEventListener('click', (e) => {
    if (!openItem) return;
    if (!openItem.contains(e.target)) closeItemEl(openItem, 0);
  });

  // --- Mobile drawer ---
  const burger = document.querySelector('.nav__burger');
  const drawer = document.querySelector('.nav__drawer');
  const closeBtn = document.querySelector('.nav__drawer-close');

  function openDrawer() {
    if (!drawer) return;
    drawer.setAttribute('data-open', 'true');
    document.body.style.overflow = 'hidden';
    burger?.setAttribute('aria-expanded', 'true');
  }

  function closeDrawer() {
    if (!drawer) return;
    drawer.setAttribute('data-open', 'false');
    document.body.style.overflow = '';
    burger?.setAttribute('aria-expanded', 'false');
  }

  burger?.addEventListener('click', openDrawer);
  closeBtn?.addEventListener('click', closeDrawer);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer?.getAttribute('data-open') === 'true') {
      closeDrawer();
      burger?.focus();
    }
  });

  // Drawer sub-menus (accordion)
  document.querySelectorAll('.nav__drawer-item[data-has-panel="true"] .nav__drawer-link').forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const item = link.closest('.nav__drawer-item');
      const isOpen = item.getAttribute('data-open') === 'true';
      item.setAttribute('data-open', isOpen ? 'false' : 'true');
    });
  });
})();
