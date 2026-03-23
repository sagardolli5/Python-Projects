from PIL import Image
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    if request.method == "POST":
        file = request.files['image']

        img = Image.open(file).convert("RGB")
        # Convert image to NumPy array
        arr = np.array(img)
        # Flatten the image - Converts 3D array → 2D list of pixels
        pixels = arr.reshape(-1, 3)
        # Find unique colors + counts
        colors, counts = np.unique(pixels, axis=0, return_counts=True)
        # Sort colors by frequency
        sorted_idx = np.argsort(counts)[::-1]
        # Get top 10 colors
        top_10_colors = colors[sorted_idx][:10]

        # Convert to HEX for display
        hex_colors = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in top_10_colors]
        return render_template("result.html", file=file.filename, colors=hex_colors)

    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)