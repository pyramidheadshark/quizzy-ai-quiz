from nicegui import ui
import os
import csv
import random

# Глобальные переменные состояния
current_card_index = 0
notification_shown = False
all_cards_viewed = False
correct_count = 0
incorrect_count = 0
flashcards = []
incorrect_cards = []
stats = {}
current_collection = None

# Функция для импорта карточек из CSV
def import_flashcards_from_csv(file_path):
    flashcards = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required_columns = {"type", "question", "correct_answer"}
            if not required_columns.issubset(reader.fieldnames):
                missing = required_columns - set(reader.fieldnames)
                ui.notify(f"Ошибка в файле {os.path.basename(file_path)}: отсутствуют колонки {missing}", type='negative')
                return []
            for row in reader:
                card = {
                    "type": row["type"],
                    "question": row["question"],
                    "correct_answer": row["correct_answer"].split(",") if "," in row["correct_answer"] else row["correct_answer"],
                    "options": row.get("options", "").split(",") if row.get("options", "") else []
                }
                flashcards.append(card)
            return flashcards
    except Exception as e:
        ui.notify(f"Не удалось загрузить файл {os.path.basename(file_path)}: {str(e)}", type='negative')
        return []

# Функция для загрузки коллекции
def load_collection(file, card_container, correct_count_label, incorrect_count_label, remaining_label):
    global flashcards, current_collection, current_card_index, notification_shown, all_cards_viewed, correct_count, incorrect_count, incorrect_cards
    flashcards = import_flashcards_from_csv(os.path.join("collections", file))
    if not flashcards:
        return
    current_collection = file
    current_card_index = 0
    notification_shown = False
    all_cards_viewed = False
    correct_count = 0
    incorrect_count = 0
    incorrect_cards = []
    correct_count_label.text = f'Правильно: {correct_count}'
    incorrect_count_label.text = f'Неправильно: {incorrect_count}'
    if current_collection not in stats:
        stats[current_collection] = {
            "total_cards": len(flashcards),
            "correct": 0,
            "incorrect": 0,
            "cards": {card["question"]: {"correct": 0, "incorrect": 0} for card in flashcards}
        }
    update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)

# Функция для повторного прохождения ошибок
def retry_incorrect_cards(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global flashcards, current_card_index, notification_shown, all_cards_viewed, correct_count, incorrect_count, incorrect_cards
    if incorrect_cards:
        flashcards = incorrect_cards.copy()
        incorrect_cards.clear()
        current_card_index = 0
        notification_shown = False
        all_cards_viewed = False
        correct_count = 0
        incorrect_count = 0
        correct_count_label.text = f'Правильно: {correct_count}'
        incorrect_count_label.text = f'Неправильно: {incorrect_count}'
        update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)
        ui.notify('Повторяем карточки с ошибками!', type='info')
    else:
        ui.notify('Нет карточек с ошибками для повторения.', type='warning')

# Функция для перезапуска всей коллекции
def restart_collection(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index, notification_shown, all_cards_viewed, correct_count, incorrect_count, incorrect_cards
    current_card_index = 0
    notification_shown = False
    all_cards_viewed = False
    correct_count = 0
    incorrect_count = 0
    incorrect_cards = []
    correct_count_label.text = f'Правильно: {correct_count}'
    incorrect_count_label.text = f'Неправильно: {incorrect_count}'
    update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)
    ui.notify(f"Коллекция '{current_collection}' перезапущена!", type='info')

# Функция для обновления содержимого карточки
def update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global notification_shown, all_cards_viewed
    if not flashcards:
        card_container.clear()
        with card_container:
            ui.label("Выберите коллекцию для начала работы.").classes('text-xl font-semibold text-center mb-4 text-gray-800 dark:text-white')
        remaining_label.text = "Осталось карточек: 0"
        return

    remaining = max(0, len(flashcards) - current_card_index)
    remaining_label.text = f"Осталось карточек: {remaining}"

    if current_card_index >= len(flashcards):
        if not notification_shown and not all_cards_viewed:
            ui.notify(f"Коллекция '{current_collection}' завершена! 🎉", type='positive')
            notification_shown = True
            all_cards_viewed = True
        card_container.clear()
        with card_container:
            with ui.column().classes('w-full text-center'):
                ui.label(f"Коллекция '{current_collection}' завершена! 🎉").classes('text-2xl font-bold mb-4 text-gray-800 dark:text-white')
                ui.label(f"Правильно: {correct_count}, Неправильно: {incorrect_count}").classes('text-lg mb-6 text-gray-800 dark:text-white')
                if incorrect_cards:
                    ui.button('Пройти ошибки заново', on_click=lambda: retry_incorrect_cards(card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-1/3 mx-auto py-2 mb-4')
                ui.button('Пройти коллекцию заново', on_click=lambda: restart_collection(card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-1/3 mx-auto py-2 mb-4')
        return

    card = flashcards[current_card_index]
    card_container.clear()
    with card_container:
        with ui.card().classes('w-3/4 mx-auto p-6 shadow-lg rounded-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-white'):
            ui.label(card["question"]).classes('text-2xl font-bold text-center mb-4 text-gray-800 dark:text-white')
            if card["type"] == "text":
                answer = ui.input('Введите ответ').classes('w-full p-2 border rounded bg-white dark:bg-gray-700 text-gray-800 dark:text-white mb-4')
                ui.button('Проверить', on_click=lambda: check_answer(answer, card, card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-full py-2 rounded')
            elif card["type"] == "single":
                selected = ui.radio(card["options"], value=None).classes('w-full flex flex-col gap-2 text-gray-800 dark:text-white mb-4')
                ui.button('Проверить', on_click=lambda: check_answer(selected, card, card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-full py-2 rounded')
            elif card["type"] == "multi":
                selected = [ui.checkbox(opt).classes('w-full text-gray-800 dark:text-white') for opt in card["options"]]
                ui.button('Проверить', on_click=lambda: check_answer(selected, card, card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-full py-2 rounded')

# Функция для проверки ответа
def check_answer(answer, card, card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index, correct_count, incorrect_count
    if card["type"] == "text":
        is_correct = answer.value.strip().lower() == card["correct_answer"].lower()
    elif card["type"] == "single":
        is_correct = answer.value == card["correct_answer"]
    elif card["type"] == "multi":
        user_answers = [cb.text for cb in answer if cb.value]
        is_correct = sorted(user_answers) == sorted(card["correct_answer"])
    
    if is_correct:
        ui.notify('Правильно! ✅', type='positive', timeout=3)
        correct_count += 1
        stats[current_collection]["correct"] += 1
        stats[current_collection]["cards"][card["question"]]["correct"] += 1
    else:
        correct_str = ", ".join(card["correct_answer"]) if isinstance(card["correct_answer"], list) else card["correct_answer"]
        ui.notify(f'Неправильно! ❌ Правильный ответ: {correct_str}', type='negative', timeout=3)
        incorrect_count += 1
        stats[current_collection]["incorrect"] += 1
        stats[current_collection]["cards"][card["question"]]["incorrect"] += 1
        if card not in incorrect_cards:
            incorrect_cards.append(card)
    correct_count_label.text = f'Правильно: {correct_count}'
    incorrect_count_label.text = f'Неправильно: {incorrect_count}'
    current_card_index += 1
    ui.timer(2.0, lambda: update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label), once=True)

# Функция для перехода к следующей карточке
def next_card(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index
    if current_card_index < len(flashcards) - 1:
        current_card_index += 1
        update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)

# Функция для перехода к предыдущей карточке
def prev_card(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index
    if current_card_index > 0:
        current_card_index -= 1
        update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)

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

# Функция для макета страницы
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
                        on_change=lambda e: load_collection(e.value, card_container, correct_count_label, incorrect_count_label, remaining_label)
                    ).classes('bg-white dark:bg-gray-700 text-gray-800 dark:text-white mt-2 w-64')
                else:
                    ui.label("Добавьте .csv файлы в папку collections").classes('text-gray-800 dark:text-white mt-2')
                card_container = ui.column().classes('w-full mt-8 flex-grow')
                with ui.row().classes('w-full mt-auto justify-between'):
                    ui.button('Предыдущая', on_click=lambda: prev_card(card_container, correct_count_label, incorrect_count_label, remaining_label)).props('icon=navigate_before').classes('bg-gray-500 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 text-white py-2 px-4 rounded')
                    ui.button('Следующая', on_click=lambda: next_card(card_container, correct_count_label, incorrect_count_label, remaining_label)).props('icon=navigate_next').classes('bg-gray-500 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 text-white py-2 px-4 rounded')
                update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)

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

    def content():
        with ui.column().classes('w-full p-4 bg-gray-100 dark:bg-gray-900 flex flex-col'):
            if not stats:
                ui.label("Статистика пока недоступна. Завершите работу с коллекцией!").classes('text-lg mb-4 text-gray-800 dark:text-white')
            else:
                for collection, data in stats.items():
                    total_attempts = data["correct"] + data["incorrect"]
                    accuracy = (data["correct"] / total_attempts * 100) if total_attempts > 0 else 0
                    with ui.card().classes('w-3/4 mx-auto p-4 shadow-lg rounded-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-white mb-4'):
                        ui.label(f"{collection}").classes('text-xl font-bold mb-2 text-gray-800 dark:text-white')
                        ui.label(f"Точность: {accuracy:.2f}% (Правильно: {data['correct']}, Неправильно: {data['incorrect']})").classes('text-lg mb-4 text-gray-800 dark:text-white')
                        for card, card_stats in data["cards"].items():
                            card_total = card_stats["correct"] + card_stats["incorrect"]
                            card_accuracy = (card_stats["correct"] / card_total * 100) if card_total > 0 else 0
                            ui.label(f"  - {card}: Точность: {card_accuracy:.2f}% (✅ {card_stats['correct']} | ❌ {card_stats['incorrect']})").classes('text-base text-gray-800 dark:text-white')

    page_layout(content)

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
