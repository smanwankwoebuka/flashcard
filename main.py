from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("../day-31-capstone-flashcard/data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

word_list = data.to_dict(orient="records")
word_dict = {}
words_to_learn = []
# ---------------------------- GENERATE RANDOM WORD ------------------------------- #


def generate_random_word():
    global timer, word_dict

    window.after_cancel(timer)
    canvas.itemconfig(image_value, image=card_front_img)
    # print(word_list)
    word_dict = random.choice(word_list)
    french_word = word_dict["French"]
    canvas.itemconfig(word_text, text=french_word, fill="black")
    canvas.itemconfig(title_text, text="French", fill="black")
    timer = window.after(3000, english_func)


# ---------------------------- ENGLISH FUNCTION ------------------------------- #


def english_func():
    canvas.itemconfig(image_value, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=word_dict["English"], fill="white")

# ---------------------------- IS KNOWN ------------------------------- #


def is_known():
    global words_to_learn, word_dict, word_list
    try:
        word_list.remove(word_dict)
    except ValueError:
        pass
    else:
        words_to_learn = pandas.DataFrame(word_list)
        words_to_learn.to_csv("../day-31-capstone-flashcard/data/words_to_learn.csv", index=False)
    finally:
        generate_random_word()
# ---------------------------- UI ------------------------------- #


window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, english_func)

card_back_img = PhotoImage(file="../day-31-capstone-flashcard/images/card_back.png")
card_front_img = PhotoImage(file="../day-31-capstone-flashcard/images/card_front.png")
right_img = PhotoImage(file="../day-31-capstone-flashcard/images/right.png")
wrong_img = PhotoImage(file="../day-31-capstone-flashcard/images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image_value = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# BUTTONS
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_random_word)
wrong_button.grid(row=1, column=0)

generate_random_word()

window.mainloop()
