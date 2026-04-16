document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.faq').forEach(faq => {
    const tabs = faq.querySelectorAll('.faq__tab');
    const panels = faq.querySelectorAll('.faq__panel');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.dataset.tab;
        tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
        tab.setAttribute('aria-selected', 'true');
        panels.forEach(p => {
          p.dataset.active = p.dataset.tab === target ? 'true' : 'false';
        });
      });
    });

    faq.querySelectorAll('.faq__question').forEach(q => {
      q.addEventListener('click', () => {
        const item = q.closest('.faq__item');
        const isOpen = item.dataset.open === 'true';
        item.dataset.open = isOpen ? 'false' : 'true';
        q.setAttribute('aria-expanded', !isOpen);
      });
    });
  });
});
