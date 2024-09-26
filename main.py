from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


def finished_cards():
    canvas.itemconfig(
        card_title, text="You've completed all the cards", fill="black")
    canvas.itemconfig(
        card_text, text="Vous avez rempli toutes les cartes", fill="black", font=("Ariel", 20, "bold"))


try:
    french_df = pandas.read_csv("data/words_to_learn.csv")
# except FileNotFoundError:
except:
    french_df = pandas.read_csv("data/french_words.csv")
    french_list = french_df.to_dict(orient="records")
else:
    french_list = french_df.to_dict(orient="records")

current_dict = {}


def translation():
    word = current_dict["English"]
    canvas.itemconfig(card_background, image=card_image_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=word, fill="white")


def new_word():
    global flip_timer
    global current_dict
    window.after_cancel(flip_timer)
    try:
        current_dict = random.choice(french_list)
    except IndexError:
        finished_cards()
    else:
        word = current_dict["French"]
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_text, text=word, fill="black")
        canvas.itemconfig(card_background, image=card_image_front)
        flip_timer = window.after(3000, translation)


def wrong_button():
    new_word()


def right_button():
    new_word()
    try:
        french_list.remove(current_dict)
    except ValueError:
        new_word()
    else:
        words_to_learn_df = pandas.DataFrame(data=french_list)
        words_to_learn_df.to_csv(
            "data/words_to_learn.csv", index=False)


window = Tk()
window.title("Flashy")
window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)


flip_timer = window.after(3000, translation)


# word
# Canvas Object || Flash Card
canvas = Canvas(width=800, height=524,
                bg=BACKGROUND_COLOR, highlightthickness=0)
card_image_front = PhotoImage(file="images/card_front.png")
card_image_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_image_front)
card_title = canvas.create_text(
    400, 150, text="", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(
    400, 263, text="", font=("Ariel", 60, "bold"))

canvas.grid(row=0, column=0, columnspan=2)

# Buttons
# X button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,
                      relief=FLAT, bg=BACKGROUND_COLOR, command=wrong_button)
wrong_button.grid(row=1, column=0)

# Y button
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0,
                      relief=FLAT, bg=BACKGROUND_COLOR, command=right_button)
right_button.grid(row=1, column=1)

new_word()

window.mainloop()
