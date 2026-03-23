import threading
from flask import Flask, render_template, request
from gtts import gTTS
import PyPDF2

app = Flask(__name__)

def convert_to_speech(text):
    tts = gTTS(text)
    tts.save("static/output.mp3")

@app.route("/", methods=["GET", "POST"])
def index():
    filename = None
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filename = file.filename

            # Extract text from PDF
            reader = PyPDF2.PdfReader(file.stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # Convert text to speech
            tts = gTTS(text)
            tts.save("static/output.mp3")

            # Run gTTS in background — don't block Flask
            thread = threading.Thread(target=convert_to_speech, args=(text,))
            thread.start()

    return render_template("index.html", filename=filename)


if __name__ == "__main__":
    app.run(debug=True)