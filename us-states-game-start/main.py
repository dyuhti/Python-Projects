import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
screen.setup(725,491)

# check whether the guess is in the state
data = pandas.read_csv("./50_states.csv")
all_states = data["state"].to_list()
guessed_states = []

# Use a loop to keep guessing
while len(guessed_states) < 50:
    # Convert the guess into Title case
    answer_state = screen.textinput(title= f"{len(guessed_states)}/50 States Correct ", prompt="What's another state's name?")
    guess = answer_state.title()

    if guess =="Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break


    #for state in all_states:
    if guess in all_states:
        guessed_states.append(guess)
    # Write correct guesses onto the map
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == guess]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(guess)










turtle.mainloop()

