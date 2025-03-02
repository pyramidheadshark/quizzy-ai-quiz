from nicegui import ui
import os

from ui.layout import page_layout
from ui.card_display import update_card_content, check_answer, next_card, prev_card
from ui.navigation import load_collection, retry_incorrect_cards_ui, restart_collection_ui
from ui.theme import initialize_theme, toggle_dark_mode
from ui.stats_display import stats_page_content
from logic.card_manager import import_flashcards_from_csv

# Initialize global state
global_state = None


# Главная страница
@ui.page('/')
def home():
    initialize_theme()

    def content():
        selected_collection = None # Define selected_collection in content scope
        selected_collection = None # Define selected_collection in outer scope
        with ui.column().classes('w-full p-4 bg-gray-100 dark:bg-gray-900 flex flex-col'):
            with ui.row().classes('w-full justify-center gap-4'):
                correct_count_label = ui.label('Правильно: 0').classes('text-green-500 text-lg dark:text-green-400')
                incorrect_count_label = ui.label('Неправильно: 0').classes('text-red-500 text-lg dark:text-red-400')
                remaining_label = ui.label('Осталось карточек: 0').classes('text-lg text-gray-800 dark:text-white')
            with ui.row().classes('w-full justify-center gap-4'):
                collections_dir = "collections"
                if not os.path.exists(collections_dir):
                    os.makedirs(collections_dir)
                collections = [f for f in os.listdir(collections_dir) if f.endswith(".csv")]
                def load_and_show_start_button(e):
                    if e.value:
                        start_button.visible = True
                        selected_collection.value = e.value # Save selected collection value for start_button

                def start_collection(card_container, file, correct_count_label, incorrect_count_label, remaining_label):
                    load_collection(file, card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content)
                    card_container.style('visibility: visible') # Show card container
                    prev_button.visible = True # Show prev button
                    next_button.visible = True # Show next button
                    start_button.visible = False # Hide start button

                selected_collection = None # Define selected_collection in the outer scope

                selected_collection = None # Define selected_collection in outer scope
                selected_collection = None # Define selected_collection in outer scope
                selected_collection = None # Define selected_collection in outer scope
                selected_collection = None

                selected_collection = None # Define selected_collection
                if collections:
                    selected_collection = ui.select(
                        options=collections,
                        label="Выберите коллекцию",
                        on_change=load_and_show_start_button
                    ).classes('bg-white dark:bg-gray-700 text-gray-800 dark:text-white mt-2 w-64')
                else:
                    ui.label("Добавьте .csv файлы в папку collections").classes('text-gray-800 dark:text-white mt-2')

                start_button = ui.button('Начать', on_click=lambda: start_collection(card_container, selected_collection.value, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-32 py-2 rounded mt-4')
                start_button.visible = False # Initially hidden

                card_container = ui.column().classes('w-full mt-8 flex-grow').style('visibility: hidden') # Initially hidden
                with ui.row().classes('w-full mt-auto justify-between').style('visibility: hidden'): # Initially hidden
                    prev_button = ui.button('Предыдущая', on_click=lambda: prev_card(card_container, correct_count_label, incorrect_count_label, remaining_label)).props('icon=navigate_before').classes('bg-gray-500 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 text-white py-2 px-4 rounded')
                    next_button = ui.button('Следующая', on_click=lambda: next_card(card_container, correct_count_label, incorrect_count_label, remaining_label)).props('icon=navigate_next').classes('bg-gray-500 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 text-white py-2 px-4 rounded')
                prev_button.visible = False # Initially hidden
                next_button.visible = False # Initially hidden
                update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label) # Initial call to show "Выберите коллекцию"

            def load_and_show_start_button(e):
                if e.value:
                    start_button.visible = True
                    selected_collection.value = e.value # Save selected collection value for start_button

            def start_collection(card_container, file, correct_count_label, incorrect_count_label, remaining_label):
                load_collection(file, card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content)
                card_container.style('visibility: visible') # Show card container
                prev_button.visible = True # Show prev button
                next_button.visible = True # Show next button
                start_button.visible = False # Hide start button


    page_layout(content)
from nicegui import ui
import os

from ui.layout import page_layout
from ui.card_display import update_card_content, check_answer, next_card, prev_card
from ui.navigation import load_collection, retry_incorrect_cards_ui, restart_collection_ui
from ui.theme import initialize_theme, toggle_dark_mode
from ui.stats_display import stats_page_content
from logic.card_manager import import_flashcards_from_csv

# Initialize global state
global_state = None


# Главная страница
@ui.page('/')
def home():
    initialize_theme()

    def content():
        with ui.column().classes('w-full p-4 bg-gray-100 dark:bg-gray-900 flex flex-col'):
            with ui.row().classes('w-full justify-center gap-4'):
                correct_count_label = ui.label('Правильно: 0').classes('text-green-500 text-lg dark:text-green-400')
                incorrect_count_label = ui.label('Неправильно: 0').classes('text-red-500 text-lg dark:text-red-400')
                remaining_label = ui.label('Осталось карточек: 0').classes('text-lg text-gray-800 dark:text-white')
            with ui.row().classes('w-full justify-center gap-4'):
                collections_dir = "collections"
                if not os.path.exists(collections_dir):
                    os.makedirs(collections_dir)
                collections = [f for f in os.listdir(collections_dir) if f.endswith(".csv")]
                if collections:
                    ui.select(
                        options=collections,
                        label="Выберите коллекцию",
                        on_change=lambda e: load_collection(e.value, card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content)
                    ).classes('bg-white dark:bg-gray-700 text-gray-800 dark:text-white mt-2 w-64')
                else:
                    ui.label("Добавьте .csv файлы в папку collections").classes('text-gray-800 dark:text-white mt-2')

                start_button = ui.button('Начать', on_click=lambda: start_collection(card_container, selected_collection.value, correct_count_label, incorrect_count_label, remaining_label, update_card_content)).classes('bg-blue-500 text-white w-32 py-2 rounded mt-4')
                start_button.visible = False

                card_container = ui.column().classes('w-full mt-8 flex-grow').style('visibility: hidden')
                with ui.row().classes('w-full mt-auto justify-between').style('visibility: hidden'):
                    prev_button = ui.button('Предыдущая', on_click=lambda: prev_card(card_container, correct_count_label, incorrect_count_label, remaining_label)).props('icon=navigate_before').classes('bg-gray-500 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 text-white py-2 px-4 rounded')
                    next_button = ui.button('Следующая', on_click=lambda: next_card(card_container, correct_count_label, incorrect_count_label, remaining_label)).props('icon=navigate_next').classes('bg-gray-500 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 text-white py-2 px-4 rounded')
                prev_button.visible = False
                next_button.visible = False
                update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)

            def load_and_show_start_button(e):
                if e.value:
                    start_button.visible = True
                    selected_collection.value = e.value

            def start_collection(card_container, file, correct_count_label, incorrect_count_label, remaining_label, update_card_content_callback):
                load_collection(file, card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content_callback)
                card_container.style('visibility: visible')
                prev_button.visible = True
                next_button.visible = True
                start_button.visible = False


    page_layout(content)

# Страница "О приложении"
@ui.page('/about')
def about():
    initialize_theme()

    def content():
        with ui.column().classes('w-full p-4 bg-gray-100 dark:bg-gray-900 flex flex-col'):
            with ui.card().classes('w-3/4 mx-auto p-6 shadow-lg rounded-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-white'):
                ui.label('О приложении').classes('text-3xl font-bold mb-4 text-gray-800 dark:text-white')
                ui.label('Это приложение для изучения с помощью флеш-карточек.').classes('text-lg text-gray-800 dark:text-white')

    page_layout(content)

# Страница статистики
@ui.page('/stats')
def stats_page():
    initialize_theme()
    page_layout(stats_page_content) # Use stats_page_content from ui/stats_display.py


# Добавление глобальных стилей
if __name__ in ('__main__', '__mp_main__'):
    ui.add_css("""
        /* Стили для тёмной темы */
        :root {
            --q-dark: #1f2937; /* Tailwind gray-800 */
            --q-light: #f3f4f6; /* Tailwind gray-100 */
        }
        html.dark {
            background-color: #111827; /* Tailwind gray-900 */
            color: #ffffff;
        }
        /* Переопределение стилей NiceGUI/Quasar */
        .q-input, .q-radio, .q-checkbox, .q-select {
            color: #374151 !important; /* gray-700 */
        }
        html.dark .q-input, html.dark .q-radio, html.dark .q-checkbox, html.dark .q-select {
            color: #ffffff !important;
            background-color: #374151 !important; /* gray-700 */
        }
        html.dark .q-select__dropdown {
            background-color: #374151 !important;
            color: #ffffff !important;
        }
        /* Улучшение кнопок */
        .q-btn {
            transition: background-color 0.3s;
        }
    """)
    ui.run()
