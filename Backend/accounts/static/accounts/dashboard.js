// Toggle sidebar
const dashboard = document.getElementById('dashboard');
const toggleSidebar = document.getElementById('toggleSidebar');

if (toggleSidebar) {
    toggleSidebar.addEventListener('click', () => {
        dashboard.classList.toggle('collapsed');
    });
}

// Toggle user dropdown
const userMenuToggle = document.getElementById('userMenuToggle');
const userDropdown = document.getElementById('userDropdown');

if (userMenuToggle && userDropdown) {
    userMenuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.hidden = !userDropdown.hidden;
    });

    // Fecha ao clicar fora
    document.addEventListener('click', (e) => {
        if (!userDropdown.hidden && !userDropdown.contains(e.target) && e.target !== userMenuToggle) {
            userDropdown.hidden = true;
        }
    });

    // Fecha com ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') userDropdown.hidden = true;
    });
}
