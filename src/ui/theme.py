from nicegui import ui

# Функция для переключения темной темы
def toggle_dark_mode(enabled):
    if enabled:
        ui.run_javascript("""
            document.documentElement.classList.add('dark');
            localStorage.setItem('darkMode', 'true');
            document.querySelectorAll('.dark-mode-switch input').forEach(input => input.checked = true);
        """)
        ui.notify("Темная тема включена!", type='positive')
    else:
        ui.run_javascript("""
            document.documentElement.classList.remove('dark');
            localStorage.setItem('darkMode', 'false');
            document.querySelectorAll('.dark-mode-switch input').forEach(input => input.checked = false);
        """)
        ui.notify("Темная тема выключена!", type='positive')

# Функция для инициализации темы при загрузке страницы
def initialize_theme():
    ui.run_javascript("""
        const darkMode = localStorage.getItem('darkMode');
        if (darkMode === 'true') {
            document.documentElement.classList.add('dark');
            document.querySelectorAll('.dark-mode-switch input').forEach(input => input.checked = true);
        } else {
            document.documentElement.classList.remove('dark');
            document.querySelectorAll('.dark-mode-switch input').forEach(input => input.checked = false);
        }
    """)
