import os
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import ttkbootstrap as tb

PINK = "#FF00FF"
GREEN = "#9bdeac"
BLACK = "#25343F"
FONT_NAME = "Segoe UI"
new_img = None
# ---------------------------- TKINTER WINDOW OBJECT ------------------------------- #
window = tb.Window(themename="flatly")
window.title("Watermarking Desktop App")
window.config(padx=100, pady=50, bg=BLACK)
# ---------------------------- UPLOAD IMAGE ------------------------------- #

def img_upload():
    global photo, new_img
    file_path = filedialog.askopenfilename(
        parent=window,
        initialdir=os.getcwd(),
        title="Select an Image",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")]
    )
    if file_path:
        new_img = Image.open(file_path)
        photo = ImageTk.PhotoImage(new_img)
        canvas.config(width=new_img.width, height=new_img.height)
        canvas.coords(canvas_image, new_img.width // 2, new_img.height // 2)
        canvas.itemconfig(canvas_image, image=photo)

# ---------------------------- UPLOAD IMAGE ------------------------------- #
def save_img():
    global new_img, photo

    file_path = filedialog.asksaveasfilename(
        parent=window,
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"),
                   ("JPEG files", "*.jpg;*.jpeg"),
                   ("All files", "*.*")],
        title="Save Image As"
    )
    if file_path:
        new_img.save(file_path)
        print(f"Image saved to: {file_path}")

# ---------------------------- ADD WATERMARK ------------------------------- #
def add_watermark():
    global new_img, photo

    watermark_path = filedialog.askopenfilename(
        title="Select Watermark Image",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")]
    )
    if watermark_path:
        watermark = Image.open(watermark_path).resize((30, 30))
        # Bottom right corner position
        x = new_img.width - 50 - 10   # 10px padding
        y = new_img.height - 50 - 10  # 10px padding
        # If watermark has transparency (PNG), use it as a mask
        if watermark.mode == "RGBA":
            new_img.paste(watermark, (x, y), mask=watermark)
        else:
            new_img.paste(watermark, (x, y))
        # Refresh canvas
        photo = ImageTk.PhotoImage(new_img)
        canvas.itemconfig(canvas_image, image=photo)
# ---------------------------- UI SETUP ------------------------------- #
my_label = tb.Label(master=window,text="Watermarking Images",font=(FONT_NAME, 34, "bold"),foreground=GREEN,background=BLACK,)
my_label.grid(column=0, row=0, columnspan=2, pady=(0, 20))

# ---------------------------- IMAGE ------------------------------- #
img = Image.open("image/picture.png")
img = img.resize((256, 256))
photo = ImageTk.PhotoImage(img)

canvas = tb.Canvas(window,width=photo.width(),height=photo.height(),background=BLACK,highlightthickness=0)
canvas_image = canvas.create_image(photo.width()//2, photo.height()//2, anchor="center", image=photo)
canvas.grid(column=0, row=1, columnspan=2, pady=(0, 20))

# ---------------------------- BUTTONS ------------------------------- #
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

# Upload Image button
upload_btn = tb.Button(window,text="Upload Image",bootstyle="primary-outline",command=img_upload)
upload_btn.grid(column=0, row=2, sticky="ew", padx=(0,5), pady=(0,10))

# Watermark button
watermark_btn = tb.Button(window,text="Add Watermark",bootstyle="primary-outline",command=add_watermark)
watermark_btn.grid(column=1, row=2, sticky="ew", padx=(5,0), pady=(0,10))

# Save button
save_btn = tb.Button(window,text="Save Image",bootstyle="primary-outline",command=save_img)
save_btn.grid(column=0, row=3, sticky="ew", padx=(0,5), pady=(0,10))

# Close button
close_btn = tb.Button(window,text="Close",bootstyle="danger",command=window.destroy)
close_btn.grid(column=1, row=3, sticky="ew", padx=(5,0), pady=(0,10))

window.mainloop()