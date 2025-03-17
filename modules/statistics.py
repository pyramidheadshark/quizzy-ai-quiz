import json
import os
from datetime import datetime
import pandas as pd

class Statistics:
    def __init__(self, storage_file: str = "data/statistics.json"):
        self.storage_file = storage_file
        self.data = self._load_data()

    def _load_data(self) -> list:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, default=str)

    def add_record(self, quiz_id: str, correct: int, total: int) -> None:
        record = {
            "quiz_id": quiz_id,
            "timestamp": datetime.now().isoformat(),
            "correct": correct,
            "total": total,
            "percentage": (correct / total) * 100 if total > 0 else 0
        }
        self.data.append(record)
        self.save_data()

    def get_statistics(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)