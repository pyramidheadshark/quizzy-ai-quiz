import csv
import os
from nicegui import ui
from logic.state_manager import current_collection

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

# Функция для проверки ответа
def check_answer(answer, card):
    if card["type"] == "text":
        return answer.value.strip().lower() == card["correct_answer"].lower()
    elif card["type"] == "single":
        return answer.value == card["correct_answer"]
    elif card["type"] == "multi":
        user_answers = [cb.text for cb in answer if cb.value]
        return sorted(user_answers) == sorted(card["correct_answer"])
    return False

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
        from ui.card_display import update_card_content # Import locally to avoid circular import
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
    from ui.card_display import update_card_content # Import locally to avoid circular import
    update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label)
    ui.notify(f"Коллекция '{current_collection}' перезапущена!", type='info')
