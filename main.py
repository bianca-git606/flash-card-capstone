from tkinter import *
import pandas as pd
import random as r
# --------------------------- CODE ---------------------------S
current_word = {}
words_dict = {}
BACKGROUND_COLOR = "#B1DDC6"

# read the csv file
try:
    with open("words_to_learn.csv") as file:
        df = pd.read_csv(file)
# if there is no existing file to load, create a new one
except FileNotFoundError:
    with open("data/french_words.csv") as file:
        df = pd.read_csv(file)
        words_dict = df.to_dict(orient="records")
# turn the dataframe into a dictionary
else:
    words_dict = df.to_dict(orient="records")


# --------------------------- FUNCTIONALITY ----------------------

def delete_word():
    # deletes the current word from the dictionary
    global current_word
    words_dict.remove(current_word)
    # writes the new set of words into a file
    data = pd.DataFrame(words_dict)
    data.to_csv("data/words_to_learn.csv")


def generate_word():
    # when buttons are pressed, it invalidates the previous timer, so that it doesn't flip prematurely
    global current_word, timer
    window.after_cancel(timer)
    # generate a new french word
    current_word = r.choice(words_dict)
    #creates the ui
    canvas.itemconfig(word_text, text=current_word["French"], fill="black")
    canvas.itemconfig(lang_text, text="French", fill="black")
    canvas.itemconfig(canv_img, image=front_card)
    # starts a new timer for the current card
    timer = window.after(3000, func=flip_card)
    print(current_word["French"] + current_word["English"])


def flip_card():
    window.after_cancel(timer)
    # Make sure to initialize the img variables outside the function
    canvas.itemconfig(canv_img, image=back_card)
    canvas.itemconfig(lang_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_word["English"], fill="white")


# --------------------------- UI SETUP ---------------------------
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# starts the timer
timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(column=0, columnspan=2, row=0)
back_card = PhotoImage(file="images/card_back.png")
front_card = PhotoImage(file="images/card_front.png")
canv_img = canvas.create_image(400, 260, image=front_card)
lang_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=lambda: [generate_word(), delete_word()])
right_button.grid(column=0, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_word)
wrong_button.grid(column=1, row=1)

generate_word()

window.mainloop()
