from nicegui import ui
from flashcards import import_flashcards_from_csv, SingleChoiceFlashcard, MultipleChoiceFlashcard, TextInputFlashcard
import random

def page_layout(content):
    with ui.header(elevated=True).classes('bg-black dark:bg-gray-900 z-index-1000 fixed top-0 w-full left-0'):
        ui.label('Флеш-карточки').classes('text-h5 text-white dark:text-black')

    with ui.left_drawer(value=True, elevated=True).classes('bg-black dark:bg-gray-900 z-index-900 fixed'):
        ui.label('Меню').classes('text-h6 text-white dark:text-black')
        ui.link('Карточки', '/').classes('text-body1 text-white dark:text-black')
        ui.link('О приложении', '/about').classes('text-body1 text-white dark:text-black')
        ui.switch('Тёмная тема', on_change=lambda e: toggle_dark_mode(e.value)).classes('q-mt-md text-white dark:text-black')

    with ui.column().classes('q-pa-md q-ml-xl q-mt-xl q-pt-xl dark:bg-black! dark:text-white!'):
        content()

current_card_index = 0
notification_shown = False

def toggle_dark_mode(enabled):
    if enabled:
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()

@ui.page('/')
def home():
    def content():
        global current_card_index, notification_shown
        flashcards = import_flashcards_from_csv('data/flashcards.csv')

        content_container = ui.column().classes('q-pa-md')

        def update_card():
            global notification_shown
            if current_card_index >= len(flashcards):
                if not notification_shown:
                    ui.notify('Все карточки просмотрены!', type='positive')
                    notification_shown = True
                return

            card = flashcards[current_card_index]
            content_container.clear()

            with content_container:
                with ui.card().classes('max-w-md mx-auto q-pa-md shadow-lg text-black dark:bg-gray-800! '):
                    ui.label(card.question).classes('text-h6 q-mb-md dark:text-white')

                    if card.card_type == 1:
                        options = [card.correct_answer] + card.incorrect_answers
                        random.shuffle(options)
                        selected = ui.radio(options, value=None).classes('q-ml-sm q-mb-sm dark:text-white')

                        def check_single():
                            global current_card_index, notification_shown
                            if selected.value == card.correct_answer:
                                ui.notify('Правильно!', type='positive')
                                ui.timer(2.0, lambda: next_card())
                            else:
                                ui.notify(f'Неправильно. Правильный ответ: {card.correct_answer}', type='negative')
                                ui.timer(2.0, lambda: next_card())

                        ui.button('Проверить', on_click=check_single).classes('q-mt-md q-mb-md').style('background-color: #4a5568 !important; color: white !important;')

                    elif card.card_type == 2:
                        options = card.correct_answers + card.incorrect_answers
                        random.shuffle(options)
                        selected = []
                        for opt in options:
                            cb = ui.checkbox(opt, value=False).classes('q-ml-sm q-mb-sm dark:text-white')
                            selected.append(cb)

                        def check_multiple():
                            global current_card_index, notification_shown
                            user_answers = [cb.text for cb in selected if cb.value]
                            if sorted(user_answers) == sorted(card.correct_answers):
                                ui.notify('Правильно!', type='positive')
                                ui.timer(2.0, lambda: next_card())
                            else:
                                correct_str = ", ".join(card.correct_answers)
                                ui.notify(f'Неправильно. Правильные ответы: {correct_str}', type='negative')
                                ui.timer(2.0, lambda: next_card())

                        ui.button('Проверить', on_click=check_multiple).classes('q-mt-md q-mb-md').style('background-color: #4a5568 !important; color: white !important;')


                    elif card.card_type == 3:
                        answer = ui.input('Введите ответ').classes('q-mt-sm q-mb-sm dark:bg-gray-700 dark:text-white')

                        def check_text():
                            global current_card_index, notification_shown
                            if answer.value.strip().lower() == card.correct_answer.lower():
                                ui.notify('Правильно!', type='positive')
                                ui.timer(2.0, lambda: next_card())
                            else:
                                ui.notify(f'Неправильно. Правильный ответ: {card.correct_answer}', type='negative')
                                ui.timer(2.0, lambda: next_card())

                        ui.button('Проверить', on_click=check_text).classes('q-mt-md q-mb-md').style('background-color: #4a5568 !important; color: white !important;')

        def next_card():
            global current_card_index
            current_card_index += 1
            update_card()

        update_card()

    page_layout(content)

@ui.page('/about')
def about():
    def content():
        with ui.column().classes('q-pa-md'):
            with ui.card().classes('max-w-md mx-auto q-pa-md shadow-lg text-black dark:bg-gray-800 dark:text-white'):
                ui.label('О приложении').classes('text-h4 q-mb-md dark:text-white')
                ui.label('Это приложение для изучения с помощью флеш-карточек.').classes('text-body1 dark:text-white')

    page_layout(content)

ui.run()
