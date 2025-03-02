from nicegui import ui

def page_layout(content):
    with ui.header(elevated=True).classes('bg-gray-800 z-index-1000 fixed top-0 w-full left-0'):
        ui.label('Флеш-карточки').classes('text-2xl font-bold text-white p-4')

    with ui.left_drawer(value=True, elevated=True).classes('bg-gray-800 z-index-900 fixed w-64 p-4 text-white'):
        ui.label('Меню').classes('text-xl font-semibold mb-4')
        ui.link('Карточки', '/').classes('text-lg mb-2')
        ui.link('О приложении', '/about').classes('text-lg mb-2')
        ui.link('Статистика', '/stats').classes('text-lg mb-4')
        ui.switch('Тёмная тема', value=False, on_change=lambda e: toggle_dark_mode(e.value)).classes('mt-4 dark-mode-switch text-white')

    with ui.column().classes('w-full p-4 bg-gray-100 dark:bg-gray-900 flex flex-col'):
        content()

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
