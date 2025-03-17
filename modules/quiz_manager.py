from modules.quiz import Quiz
from modules.quiz_generator import QuizGenerator
from modules.data_storage import JsonDataStorage

class QuizManager:
    def __init__(self, storage: JsonDataStorage, generator: QuizGenerator):
        self.storage = storage
        self.generator = generator

    def create_quiz(self, title: str, theme: str, material: str, language: str, difficulty: str, num_questions: int) -> Quiz:
        questions = self.generator.generate_questions(theme, material, language, difficulty, num_questions)
        quiz = Quiz.create(title, theme, material, questions)
        self.storage.save_quiz(quiz)
        return quiz

    def get_quiz(self, quiz_id: str) -> Quiz:
        return self.storage.load_quiz(quiz_id)

    def list_quizzes(self) -> list:
        return self.storage.list_quizzes()

    def list_quiz_titles(self) -> dict:
        """Return a dictionary of quiz IDs mapped to their titles."""
        quizzes = self.list_quizzes()
        titles = {}
        for quiz_id in quizzes:
            quiz = self.get_quiz(quiz_id)
            titles[quiz_id] = quiz.title
        return titles

    def rename_quiz(self, quiz_id: str, new_title: str) -> None:
        quiz = self.get_quiz(quiz_id)
        quiz.title = new_title
        self.storage.save_quiz(quiz)

    def delete_quiz(self, quiz_id: str) -> None:
        self.storage.delete_quiz(quiz_id)