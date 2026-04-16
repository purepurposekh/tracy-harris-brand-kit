// Navigation — hover + click to open dropdowns. Keyboard accessible.
(function () {
  const items = document.querySelectorAll('.nav__item[data-has-panel="true"]');
  if (!items.length) return;

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

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!openItem) return;
    if (!openItem.contains(e.target)) {
      closeItemEl(openItem, 0);
    }
  });
})();
