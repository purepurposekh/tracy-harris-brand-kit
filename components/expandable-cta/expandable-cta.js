document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.expandable-cta').forEach(cta => {
    const trigger = cta.querySelector('.expandable-cta__trigger-btn');
    const overlay = cta.querySelector('.expandable-cta__overlay');
    const close = cta.querySelector('.expandable-cta__close');

    if (!trigger || !overlay) return;

    function open() {
      overlay.dataset.open = 'true';
      document.body.style.overflow = 'hidden';
      setTimeout(() => {
        const first = overlay.querySelector('input, textarea');
        if (first) first.focus();
      }, 400);
    }

    function shut() {
      overlay.dataset.open = 'false';
      document.body.style.overflow = '';
      trigger.focus();
    }

    trigger.addEventListener('click', open);
    if (close) close.addEventListener('click', shut);

    overlay.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') shut();
    });

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) shut();
    });
  });
});
