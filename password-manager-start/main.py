from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
FONT_NAME = "Courier"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'
        ,'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S'
        ,'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters

    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)




# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website:{
            "email": email,
            "password": password
        }

    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Make sure that you haven't left any fields empty")
    else:


        try:
            with open("data.json", "r") as data_file:
                # Reading old Data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0,END)
            password_input.delete(0,END)

def find_password():
    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:{email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No data file found")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# logo
canvas = Canvas(width=200, height=189)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=logo_img)
canvas.grid(column=1, row=0)

# Label-website
website_label = Label(text="Website:", font=(FONT_NAME, 12))
website_label.grid(column=0, row=1)

# Label-Email
email_label = Label(text="Email/Username:", font=(FONT_NAME, 12))
email_label.grid(column=0, row=2)

# Label- password
password_label = Label(text="Password:", font=(FONT_NAME, 12))
password_label.grid(column=0, row=3)

# Button-Search
search_button = Button(text="Search", font=(FONT_NAME, 12), width=20, command=find_password)
search_button.grid(column=2, row=1)

# Button-GeneratePassword
generate_password_button = Button(text="Generate Password", font=(FONT_NAME, 12), width= 20, command=generate_password)
generate_password_button.grid(column=2, row=3)

# Button-add
add_button = Button(text="Add",font=(FONT_NAME,12), width=41, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# Entry-website
website_input = Entry(width=32)
website_input.grid(column=1, row=1)
website_input.focus()

# Entry-email
email_input = Entry(width=68)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(0, "")

# Entry-password
password_input = Entry(width=32)
password_input.grid(column=1, row=3)

window.mainloop()
