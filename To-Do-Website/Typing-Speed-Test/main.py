import time
import requests
import ttkbootstrap as tb
from PIL import Image, ImageTk
from tkinter import Text

PINK = "#FF00FF"
GREEN = "#9bdeac"
BLACK = "#25343F"
FONT_NAME = "Segoe UI"
# Counter to track the number of incorrectly typed or missing characters
wrong_keystrokes = 0

# Quotable API - Returns random quotes
response = requests.get("https://zenquotes.io/api/random")

# ---------------------------- BACK TO HOME ------------------------------- #
def reset():
    my_label.config(text="Typing Speed Test")  # reset title
    # Remove all result widgets
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) >= 1:
            widget.grid_remove()

    # Show the original canvas and buttons
    canvas.grid(column=0, row=1, columnspan=2, pady=(0, 20))
    type_btn.grid(column=0, row=2, pady=20)
    close_btn.grid(column=1, row=2, pady=20)

# ---------------------------- Typing Text ------------------------------- #
def target_text():
    type_btn.grid_remove()
    close_btn.grid_remove()
    canvas.grid_remove()
    quote = response.json()[0]["q"]

    # Fixed size frame for quote label
    label_frame = tb.Frame(window, width=450, height=100)
    label_frame.grid(column=0, row=1, columnspan=2, padx=20, pady=20)
    label_frame.grid_propagate(False)  # locks the size

    label = tb.Label(
        label_frame,
        text=quote,
        font=(FONT_NAME, 14),
        wraplength=500,
        justify="center",
        background="white",
        padding=20,
    )
    label.place(x=0, y=0, width=450, height=100)  # place fills the entire frame

    # Record the exact time before the user starts typing
    start_time = time.time()

    # Fixed size frame for entry box
    entry_frame = tb.Frame(window, width=450, height=100)
    entry_frame.grid(column=0, row=2, columnspan=2, padx=20, pady=(0, 20))
    entry_frame.grid_propagate(False)  # locks the size

    entry_box = Text(
        entry_frame,
        font=(FONT_NAME, 14),
        wrap="word",
        relief="flat",
        bg="#2E4057",
        fg="white",
        padx=15,
        pady=15,
        bd=0,
        insertbackground="white",
    )
    entry_box.insert("1.0", "Start typing here...")
    entry_box.bind("<Key>", lambda e: entry_box.delete("1.0", "end") or entry_box.unbind("<Key>"))
    entry_box.place(x=0, y=0, width=450, height=100)
    entry_box.focus()

    # Submit button
    submit_btn = tb.Button(
        window,
        text="Submit",
        bootstyle="success",
        command=lambda: display_result(*check_text(entry_box.get("1.0", "end-1c"), quote, start_time), label_frame, entry_frame, submit_btn)
    )
    submit_btn.grid(column=0, row=3, columnspan=2, pady=20)


def check_text(user_text, prompt_text, initial_time):
    global wrong_keystrokes
    wrong_keystrokes = 0  # reset every time
    # Calculate how many seconds the user took to type
    elapsed_seconds = time.time() - initial_time
    # Convert seconds to minutes as WPM formula requires time in minutes
    elapsed_minutes = elapsed_seconds / 60

    # Compare each character of the target text with the user's input
    # If the user typed fewer characters than the target, count the rest as errors
    # If the character doesn't match the target, count it as an error
    for i in range(len(prompt_text)):
        if i >= len(user_text):
            wrong_keystrokes += 1
        elif prompt_text[i] != user_text[i]:
            wrong_keystrokes += 1

    # Gross WPM: total characters typed divided by 5 (standard word length), divided by time
    gross_wpm = (len(user_text) / 5) / elapsed_minutes
    # Accuracy: percentage of correctly typed characters out of the total target characters
    accuracy = ((len(prompt_text) - wrong_keystrokes) / len(prompt_text)) * 100
    # Net WPM: Gross WPM minus the error penalty
    net_wpm = gross_wpm - (wrong_keystrokes / elapsed_minutes)

    return gross_wpm, net_wpm ,accuracy


def display_result(gross_wpm, net_wpm, accuracy, display_frame, entry_box, done_btn):
    my_label.config(text="Your Results")  # update title
    my_label.grid(column=0, row=0, columnspan=4, pady=(0, 20))

    display_frame.grid_remove()
    entry_box.grid_remove()
    done_btn.grid_remove()

    results = [
        ("Gross WPM", round(gross_wpm)),
        ("Net WPM", round(net_wpm)),
        ("Errors", wrong_keystrokes),
        ("Accuracy", f"{round(accuracy)}%"),
    ]

    for i, (title, value) in enumerate(results):
        box = tb.Frame(window, width=200, height=80)
        box.grid(column=i, row=4, padx=10, pady=30)
        box.grid_propagate(False)

        tb.Label(
            box,
            text=f"{title}\n{value}",
            font=(FONT_NAME, 14, "bold"),
            background="#2E4057",
            foreground="White",
            justify="center",
            anchor="center",
        ).place(x=0, y=0, width=200, height=80)

    back_btn = tb.Button(
        window,
        text="← Back",
        bootstyle="primary-outline",
        command=reset
    )
    back_btn.grid(column=0, row=5, columnspan=4, pady=10)

# ---------------------------- TKINTER WINDOW OBJECT ------------------------------- #
window = tb.Window(themename="flatly")
window.title("Watermarking Desktop App")
window.config(padx=100, pady=50, bg=BLACK)

# ---------------------------- UI SETUP ------------------------------- #
my_label = tb.Label(master=window,text="Typing Speed Test",font=(FONT_NAME, 34, "bold"),foreground=GREEN,background=BLACK,)
my_label.grid(column=0, row=0, columnspan=2, pady=(0, 20))

# ---------------------------- IMAGE ------------------------------- #
img = Image.open("image/typing.png").convert("RGBA")
img = img.resize((256, 256))
bg = Image.new("RGBA", img.size, BLACK)
bg.paste(img, (0, 0), img)
photo = ImageTk.PhotoImage(bg)

canvas = tb.Canvas(window,width=photo.width(),height=photo.height(),background=BLACK,highlightthickness=0)
canvas_image = canvas.create_image(photo.width()//2, photo.height()//2, anchor="center", image=photo)
canvas.grid(column=0, row=1, columnspan=2, pady=(0, 20))

# ---------------------------- BUTTONS ------------------------------- #
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

# Typing button
type_btn = tb.Button(window,text="Start Typing",bootstyle="primary-outline", command=target_text)
type_btn.grid(column=0, row=2, sticky="ew", padx=(0,5), pady=(0,10))

# Close button
close_btn = tb.Button(window,text="Close",bootstyle="danger",command=window.destroy)
close_btn.grid(column=1, row=2, sticky="ew", padx=(5,0), pady=(0,10))

window.mainloop()