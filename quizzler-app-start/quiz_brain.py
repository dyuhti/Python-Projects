class QuizBrain:
    def __init__(self, question_data):
        self.question_list = question_data
        self.question_number = 0
        self.score = 0  # Add this line

    def next_question(self):
        question = self.question_list[self.question_number]["question"]
        self.question_number += 1
        return question

    def check_answer(self, user_answer):
        correct_answer = self.question_list[self.question_number - 1]["correct_answer"]
        if user_answer.lower() == correct_answer.lower():
            self.score += 1  # Increment the score when the answer is correct
            return True
        else:
            return False

    def still_has_questions(self):
        return self.question_number < len(self.question_list)