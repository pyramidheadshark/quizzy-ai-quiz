import csv

class Flashcard:
    def __init__(self, question, card_type):
        self.question = question
        self.card_type = card_type

class SingleChoiceFlashcard(Flashcard):
    def __init__(self, question, correct_answer, incorrect_answers):
        super().__init__(question, 1)
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers

class MultipleChoiceFlashcard(Flashcard):
    def __init__(self, question, correct_answers, incorrect_answers):
        super().__init__(question, 2)
        self.correct_answers = correct_answers
        self.incorrect_answers = incorrect_answers

class TextInputFlashcard(Flashcard):
    def __init__(self, question, correct_answer):
        super().__init__(question, 3)
        self.correct_answer = correct_answer

def import_flashcards_from_csv(file_path):
    flashcards = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            question, card_type = row[0], int(row[1])
            if card_type == 1:
                correct_answer = row[2]
                incorrect_answers = row[3:]
                flashcards.append(SingleChoiceFlashcard(question, correct_answer, incorrect_answers))
            elif card_type == 2:
                correct_answers = row[2].split('|')
                incorrect_answers = row[3:]
                flashcards.append(MultipleChoiceFlashcard(question, correct_answers, incorrect_answers))
            elif card_type == 3:
                correct_answer = row[2]
                flashcards.append(TextInputFlashcard(question, correct_answer))
    return flashcards