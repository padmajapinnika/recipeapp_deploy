document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.querySelector('.toggle-details-btn');
  const detailsDiv = toggleBtn.nextElementSibling;

  toggleBtn.addEventListener('click', () => {
    if (detailsDiv.style.display === 'none' || detailsDiv.style.display === '') {
      detailsDiv.style.display = 'block';
      toggleBtn.textContent = 'Hide Ingredients';
    } else {
      detailsDiv.style.display = 'none';
      toggleBtn.textContent = 'Show Ingredients';
    }
  });
});
