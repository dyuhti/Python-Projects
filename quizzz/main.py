from ui import QuizInterface
from brain import QuizzBrain
from data import question_data

quiz = QuizzBrain(question_data)
quiz_ui = QuizInterface(quiz)
quiz_ui.mainloop()