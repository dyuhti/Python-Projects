from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizler")
        self.window.config(padx=20, pady=20)

        self.canvas = Canvas(width=300,  height=230, bg="white")
        self.question_text = self.canvas.create_text(150, 125, text="Some question", fill=THEME_COLOR, width=280, font=("Arial", 20, "italic"))
        self.canvas.grid(row=1, column=0, columnspan=2)

        self.score_label = Label(text="Score:0", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=self.true_image, command=self.true_pressed)
        self.true_button.grid(column=0, row=2)

        self.false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=self.false_image, command=self.false_pressed)
        self.false_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.itemconfig(self.question_text, text=self.quiz.next_question())
        self.score_label.config(text=f"Score: {self.quiz.score}")

    def true_pressed(self):
        self.quiz.check_answer("True")
        self.get_next_question()

    def false_pressed(self):
        self.quiz.check_answer("False")
        self.get_next_question()