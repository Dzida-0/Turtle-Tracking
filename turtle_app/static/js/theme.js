 function switchTheme(theme) {
    document.documentElement.className = theme;
    localStorage.setItem('theme', theme); // Save the theme in localStorage
  }

  // Apply the saved theme on page load
  document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'theme-1';
    document.documentElement.className = savedTheme;
  });