import json
import os
from modules.quiz import Quiz

class JsonDataStorage:
    def __init__(self, storage_dir: str = "data/quizzes"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_quiz(self, quiz: Quiz) -> None:
        file_path = os.path.join(self.storage_dir, f"{quiz.id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(quiz.to_dict(), f, indent=4, default=str)

    def load_quiz(self, quiz_id: str) -> Quiz:
        file_path = os.path.join(self.storage_dir, f"{quiz_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Quiz(**data)
        raise FileNotFoundError(f"Quiz with ID {quiz_id} not found")

    def list_quizzes(self) -> list:
        return [f.split(".")[0] for f in os.listdir(self.storage_dir) if f.endswith(".json")]

    def delete_quiz(self, quiz_id: str) -> None:
        file_path = os.path.join(self.storage_dir, f"{quiz_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"Quiz with ID {quiz_id} not found")