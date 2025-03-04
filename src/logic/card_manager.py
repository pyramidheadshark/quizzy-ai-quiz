import csv
import os
from nicegui import ui
from logic.state_manager import current_collection

# Функция для импорта карточек из CSV
def import_flashcards_from_csv(file_path):
    flashcards = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f: # Changed encoding to utf-8-sig
            reader = csv.DictReader(f)
            required_columns = {"type", "question", "correct_answer"}
            if not required_columns.issubset(reader.fieldnames):
                missing = required_columns - set(reader.fieldnames)
                ui.notify(f"Ошибка в файле {os.path.basename(file_path)}: отсутствуют колонки {missing}", type='negative')
                return []
            for row in reader:
                print(f"Processing row: {row}") # Вывод текущей строки
                type_val = row["type"]
                question_val = row["question"]
                correct_answer_str = row["correct_answer"]
                options_str = row.get("options", "")
                print(f"  type_val: {type_val}, question_val: {question_val}, correct_answer_str: {correct_answer_str}, options_str: {options_str}") # Вывод значений переменных

                correct_answer_val = correct_answer_str.split(",") if "," in correct_answer_str else correct_answer_str
                options_val = options_str.split(",") if options_str else []
                print(f"  correct_answer_val: {correct_answer_val}, options_val: {options_val}") # Вывод значений после split

                card = {
                    "type": type_val,
                    "question": question_val,
                    "correct_answer": correct_answer_val,
                    "options": options_val
                }
                print(f"  card object created: {card}") # Вывод созданного объекта card
                flashcards.append(card)
                print("  Card appended to flashcards list") # Подтверждение добавления в список
            return flashcards
    except Exception as e:
        print(f"Exception: {e}") # Debug output: print exception
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
