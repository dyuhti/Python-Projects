import random
from tkinter import *
from brain import QuizzBrain

THEME_COLOR = "#000000"
TEXT_COLOR = "#FFFFFF"
PURPLE_COLOR = "#800080"

class QuizInterface:
    def __init__(self, brain: QuizzBrain):
        self.quiz = brain
        self.window = Tk()
        self.window.title("Quizzzz")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.canvas = Canvas(width=550, height=230, bg=THEME_COLOR, highlightthickness=0)
        self.question_text = self.canvas.create_text(250, 100, text="Ready for a quiz?", fill=TEXT_COLOR, width=280, font=("Arial", 20, "italic"))
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)

        self.score_label = Label(text="Score: 0", fg=TEXT_COLOR, bg=THEME_COLOR, font=("Arial", 12))
        self.score_label.grid(row=0, column=2)

        self.start_img = PhotoImage(file="images/start.png")
        self.start_button = Button(image=self.start_img, text="Let's go!", command=self.start_quiz, bg=THEME_COLOR, fg=TEXT_COLOR, highlightbackground=THEME_COLOR)
        self.start_button.grid(column=0, row=2, columnspan=2, pady=20)

        self.option_buttons = []
        for i in range(4):
            button = Button(text="", width=30, command=lambda i=i: self.check_answer(i), bg=THEME_COLOR, fg=TEXT_COLOR, highlightbackground=THEME_COLOR)
            button.grid(row=3 + i, column=0, columnspan=2, pady=5)
            button.grid_remove()
            self.option_buttons.append(button)

    def start_quiz(self):
        self.start_button.grid_remove()
        self.canvas.config(bg=PURPLE_COLOR)
        self.canvas.itemconfig(self.question_text, fill=TEXT_COLOR)
        for button in self.option_buttons:
            button.grid()
        self.get_next_question()

    def get_next_question(self):
        if self.quiz.still_has_questions():
            question = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=question["question"])
            self.score_label.config(text=f"Score: {self.quiz.score}")
            answers = question["incorrect_answers"] + [question["correct_answer"]]
            random.shuffle(answers)
            for i, option in enumerate(answers):
                self.option_buttons[i].config(text=option, state="normal")
        else:
            self.canvas.itemconfig(self.question_text, text="You've completed the quiz!")
            for button in self.option_buttons:
                button.config(state="disabled")

    def check_answer(self, index):
        user_answer = self.option_buttons[index].cget("text")
        if self.quiz.check_answer(user_answer):
            self.score_label.config(text=f"Score: {self.quiz.score}")
        self.get_next_question()

    def mainloop(self):
        self.window.mainloop()