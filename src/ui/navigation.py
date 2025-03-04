from nicegui import ui
import os

from logic.card_manager import import_flashcards_from_csv # Import card import logic
from logic.state_manager import current_card_index, notification_shown, all_cards_viewed, correct_count, incorrect_count, flashcards, incorrect_cards, stats, current_collection # Import state variables


# Функция для загрузки коллекции
def load_collection(file, card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content):
    global flashcards, current_collection, current_card_index, notification_shown, all_cards_viewed, correct_count, incorrect_count, incorrect_cards
    filepath = os.path.join("collections", file) # Store filepath in variable
    global flashcards # Declare flashcards as global
    flashcards = import_flashcards_from_csv(filepath) # Assign result to global flashcards
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
def retry_incorrect_cards(card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content): # Modified signature
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
        update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label) # Modified call
        ui.notify('Повторяем карточки с ошибками!', type='info')
    else:
        ui.notify('Нет карточек с ошибками для повторения.', type='warning')

# Функция для перезапуска всей коллекции
def restart_collection(card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content): # Modified signature
    global current_card_index, notification_shown, all_cards_viewed, correct_count, incorrect_count, incorrect_cards
    current_card_index = 0
    notification_shown = False
    all_cards_viewed = False
    correct_count = 0
    incorrect_count = 0
    incorrect_cards = []
    correct_count_label.text = f'Правильно: {correct_count}'
    incorrect_count_label.text = f'Неправильно: {incorrect_count}'
    update_card_content(card_container, correct_count_label, incorrect_count_label, remaining_label) # Modified call
    ui.notify(f"Коллекция '{current_collection}' перезапущена!", type='info')

def retry_incorrect_cards_ui(card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content):
    retry_incorrect_cards(card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content) # Modified call to pass update_card_content directly

def restart_collection_ui(card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content):
    restart_collection(card_container, correct_count_label, incorrect_count_label, remaining_label, update_card_content) # Modified call to pass update_card_content directly
