import uuid
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Quiz:
    id: str
    title: str
    theme: str
    created_at: datetime
    material: str  # Source material (text, file content, or URL)
    questions: list  # List of dicts with question, options, and correct_answer

    @classmethod
    def create(cls, title: str, theme: str, material: str, questions: list) -> "Quiz":
        """Create a new Quiz instance with a unique ID."""
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            theme=theme,
            created_at=datetime.now(),
            material=material,
            questions=questions
        )

    def to_dict(self) -> dict:
        return asdict(self)