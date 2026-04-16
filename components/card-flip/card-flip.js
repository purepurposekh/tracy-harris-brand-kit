document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.card-flip').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('a')) return;
      card.classList.toggle('is-flipped');
    });

    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.classList.toggle('is-flipped');
      }
    });
  });
});
