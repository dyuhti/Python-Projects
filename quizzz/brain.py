class QuizzBrain:
    def __init__(self,question_data):
        self.current_question = None
        self.question_list = question_data
        self.question_number = 0
        self.score = 0


    def next_question(self):
        if self.question_number < len(self.question_list):
            self.current_question = self.question_list[self.question_number]
            self.question_number += 1
            return self.current_question
        else:
            return "You've completed the quiz!"

    def check_answer(self,user_answer):
        correct_answer = self.question_list[self.question_number-1]["correct_answer"]
        if user_answer.lower() == correct_answer.lower():
            self.score+=1
            return True
        else:
            return False

    def still_has_questions(self):
        return self.question_number <len(self.question_list)
