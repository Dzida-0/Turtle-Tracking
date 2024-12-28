document.addEventListener('DOMContentLoaded', () => {
    const themeSelect = document.getElementById('theme-select');
    const themeStylesheet = document.getElementById('theme-stylesheet');

    themeSelect.addEventListener('change', (event) => {
        const selectedTheme = event.target.value;
        themeStylesheet.href = `static/${selectedTheme}.scss`;
    });
});
