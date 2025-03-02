from nicegui import ui
from logic.card_manager import check_answer # Import check_answer from logic
from logic.state_manager import current_card_index, flashcards, current_collection, notification_shown, all_cards_viewed, correct_count, incorrect_count, incorrect_cards, stats # Import state variables
from ui.navigation import retry_incorrect_cards_ui, restart_collection_ui # Import navigation UI functions

def update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global notification_shown, all_cards_viewed, current_card_index, flashcards, current_collection
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
                    ui.button('Пройти ошибки заново', on_click=lambda: retry_incorrect_cards_ui(card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-1/3 mx-auto py-2 mb-4') # Use ui function
                ui.button('Пройти коллекцию заново', on_click=lambda: restart_collection_ui(card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-1/3 mx-auto py-2 mb-4') # Use ui function
        return

    card = flashcards[current_card_index]
    card_container.clear()
    with card_container:
        with ui.card().classes('w-3/4 mx-auto p-6 shadow-lg rounded-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-white'):
            ui.label(card["question"]).classes('text-2xl font-bold text-center mb-4 text-gray-800 dark:text-white')
            if card["type"] == "text":
                answer = ui.input('Введите ответ').classes('w-full p-2 border rounded bg-white dark:bg-gray-700 text-gray-800 dark:text-white mb-4')
                ui.button('Проверить', on_click=lambda: check_answer_ui(answer, card, card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-full py-2 rounded') # Use ui function
            elif card["type"] == "single":
                selected = ui.radio(card["options"], value=None).classes('w-full flex flex-col gap-2 text-gray-800 dark:text-white mb-4')
                ui.button('Проверить', on_click=lambda: check_answer_ui(selected, card, card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-full py-2 rounded') # Use ui function
            elif card["type"] == "multi":
                selected = [ui.checkbox(opt).classes('w-full text-gray-800 dark:text-white') for opt in card["options"]]
                ui.button('Проверить', on_click=lambda: check_answer_ui(selected, card, card_container, correct_count_label, incorrect_count_label, remaining_label)).classes('bg-blue-500 text-white w-full py-2 rounded') # Use ui function

def check_answer_ui(answer, card, card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index, correct_count, incorrect_count
    is_correct = check_answer(answer, card) # Call logic function to check answer
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

def next_card(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index
    if current_card_index < len(flashcards) - 1:
        current_card_index += 1
        update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)

def prev_card(card_container, correct_count_label, incorrect_count_label, remaining_label):
    global current_card_index
    if current_card_index > 0:
        current_card_index -= 1
        update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)
