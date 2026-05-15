const dashboard = document.getElementById('dashboard');
const toggleSidebar = document.getElementById('toggleSidebar');

toggleSidebar.addEventListener('click', () => {
    dashboard.classList.toggle('collapsed');
});