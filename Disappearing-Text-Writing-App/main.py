import ttkbootstrap as tb
from PIL import Image, ImageTk
from tkinter import Text

PINK = "#FF00FF"
RED = "#D02752"
BLACK = "#25343F"
FONT_NAME = "Segoe UI"
after_id = None
# ---------------------------- BACK TO HOME ------------------------------- #
def reset():
    # Remove all result widgets
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) >= 1:
            widget.grid_remove()

    # Show the original canvas and buttons
    canvas.grid(column=0, row=1, columnspan=2, pady=(0, 20))
    type_btn.grid(column=0, row=2, pady=20)
    close_btn.grid(column=1, row=2, pady=20)

# ---------------------------- Event handler function ------------------------------- #
# Function to clear the text box
def clear_text(text_box):
    text_box.delete("1.0", "end-1c")

# Function to change text color to red
def turn_text_red(text_box):
    global after_id
    text_box.config(fg="red")
    if after_id:
        window.after_cancel(after_id)
    after_id = window.after(5000, lambda: clear_text(text_box))

# Function called when user stops typing
def stopped_typing(text_box):
    global after_id
    if after_id:
        window.after_cancel(after_id)
    after_id =window.after(5000, lambda: turn_text_red(text_box))

# Function called on every key release
def on_typing(event, text_box):
    global after_id
    text_box.config(fg="black")
    text = event.widget.get("1.0", "end-1c")
    # reset the timer
    if after_id:
        window.after_cancel(after_id)
    after_id = window.after(1000, lambda: stopped_typing(text_box))

# ---------------------------- Typing Text ------------------------------- #
def target_text():
    type_btn.grid_remove()
    close_btn.grid_remove()
    canvas.grid_remove()

    # Fixed size frame for entry box
    entry_frame = tb.Frame(window, width=550, height=200)
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
    entry_box.place(x=0, y=0, width=550, height=200)
    entry_box.focus()

    # Event = < KeyRelease > (user releases a key), Function = on_typing
    entry_box.bind("<KeyRelease>", lambda event: on_typing(event, entry_box))

    back_btn = tb.Button(window,text="← Back",bootstyle="primary-outline",command=reset)
    back_btn.grid(column=0, row=5, columnspan=4, pady=10)


# ---------------------------- TKINTER WINDOW OBJECT ------------------------------- #
window = tb.Window(themename="flatly")
window.title("Watermarking Desktop App")
window.config(padx=100, pady=50, bg=BLACK)

# ---------------------------- UI SETUP ------------------------------- #
my_label = tb.Label(master=window,text="Dangerous Writing App",font=(FONT_NAME, 34, "bold"),foreground=RED,background=BLACK,)
my_label.grid(column=0, row=0, columnspan=2, pady=(0, 20))

# ---------------------------- IMAGE ------------------------------- #
img = Image.open("img/typography.png").convert("RGBA")
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
type_btn = tb.Button(window,text="Start Typing",bootstyle="btn-info", command=target_text)
type_btn.grid(column=0, row=2, sticky="ew", padx=(0,5), pady=(0,10))

# Close button
close_btn = tb.Button(window,text="Close",bootstyle="danger",command=window.destroy)
close_btn.grid(column=1, row=2, sticky="ew", padx=(5,0), pady=(0,10))

window.mainloop()