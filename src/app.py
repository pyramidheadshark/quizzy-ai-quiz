from nicegui import ui
from flashcards import import_flashcards_from_csv, SingleChoiceFlashcard, MultipleChoiceFlashcard, TextInputFlashcard
import random

# Глобальная шапка
with ui.header(elevated=True).style('background-color: #3f51b5; z-index: 1000; position: fixed; top: 0; width: 100%;'):
    ui.label('Флеш-карточки').classes('text-h5 text-white')
    ui.label('Шапка активна').classes('text-caption text-white')  # Для отладки
    print("Шапка инициализирована")  # Для отладки

# Глобальная боковая панель
with ui.left_drawer(value=True, elevated=True).style('background-color: #f0f0f0; z-index: 900; width: 300px; position: fixed;'):
    ui.label('Меню').classes('text-h6')
    ui.link('Карточки', '/').classes('text-body1')
    ui.link('О приложении', '/about').classes('text-body1')
    ui.switch('Тёмная тема', on_change=lambda: ui.dark_mode().toggle())
    ui.label('Панель активна').classes('text-caption')  # Для отладки
    print("Боковая панель инициализирована")  # Для отладки

# Страницы
@ui.page('/')
def home():
    global current_card_index, notification_shown
    flashcards = import_flashcards_from_csv('data/flashcards.csv')
    current_card_index = 0
    notification_shown = False

    content_container = ui.column().classes('q-pa-md q-ml-xl')


@ui.page('/about')
def about():
    with ui.column().classes('q-pa-md'):
        with ui.card().classes('max-w-md mx-auto q-pa-md shadow-lg'):
            ui.label('О приложении').classes('text-h4 q-mb-md')
            ui.label('Это приложение для изучения с помощью флеш-карточек.').classes('text-body1')

ui.run()