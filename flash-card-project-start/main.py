import time
from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
fr_words = {}
to_learn = {}
try:
    data = pandas.read_csv("./data/Words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
def next_card():
    global fr_words, flip_timer
    window.after_cancel(flip_timer)
    fr_words = random.choice(to_learn)
    canvas.itemconfig(front_title, text="French")
    canvas.itemconfig(front_word, text=fr_words["French"])
    canvas.itemconfig(card_background, image=front_flashcard_image)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(front_title, text="English")
    canvas.itemconfig(front_word, text=fr_words["English"])
    canvas.itemconfig(card_background, image=back_flashcard_image)

def is_known():
    to_learn.remove(fr_words)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/Words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Flash cards-Front
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_flashcard_image = PhotoImage(file="./images/card_front.png")
back_flashcard_image = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_flashcard_image)
front_word = canvas.create_text(400, 263, text=" ", font=("Ariel", 20, "bold"))
front_title = canvas.create_text(400, 150, text=" ", font=("Ariel", 40, "italic"))
canvas.grid(column=0, row=0, columnspan=2)

# Option- Checkmark
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)

right_button.grid(column=0, row=1)

# Option- Wrong
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()


