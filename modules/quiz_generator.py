import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class QuizGenerator:
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
        self.config = GenerationConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=64,
            max_output_tokens=65536,
            response_mime_type="text/plain",
        )

    def generate_questions(self, theme: str, material: str, language: str, difficulty: str, num_questions: int) -> list:
        # Prepared for chain prompting in the future:
        # Step 1: Could generate intermediate topics or outlines (not implemented yet)
        # Step 2: Generate questions based on those topics (not implemented yet)
        # Current implementation: Single prompt for all questions
        prompt = (
            f"Generate {num_questions} multiple-choice quiz questions in {language} based on the theme '{theme}' "
            f"and the following material:\n\n{material}\n\n"
            f"Questions should be of {difficulty} difficulty (e.g., easy, medium, hard).\n"
            "For each question, provide:\n"
            "- The question text\n"
            "- Four answer options (A, B, C, D)\n"
            "- The correct answer (e.g., 'A')\n\n"
            "Ensure questions are clear, relevant, and appropriately challenging based on the difficulty level.\n"
            "Format the output as:\n"
            "1. Question text\nA) Option1\nB) Option2\nC) Option3\nD) Option4\nCorrect: A\n\n"
        )
        try:
            response = self.client.generate_content(contents=[prompt], generation_config=self.config)
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Ошибка генерации вопросов: {str(e)}")

    def _parse_response(self, text: str) -> list:
        questions = []
        lines = text.strip().split("\n")
        current_question = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Correct:"):
                current_question["correct_answer"] = line.split("Correct:")[1].strip()
                questions.append(current_question)
                current_question = {}
            elif line and line[0].isdigit() and "." in line:
                current_question["question"] = line.split(".", 1)[1].strip()
                current_question["options"] = []
            elif line and line[0] in "ABCD" and ")" in line:
                current_question["options"].append(line.split(")", 1)[1].strip())
        return questions