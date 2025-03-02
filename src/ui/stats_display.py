from nicegui import ui
from logic.state_manager import stats # Import stats variable

def stats_page_content():
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
