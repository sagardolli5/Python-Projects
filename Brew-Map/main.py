from flask import Flask, render_template, request
import requests

URL = "https://api.openbrewerydb.org/v1/breweries"
app = Flask(__name__)

@app.route("/")
def index():
    page = request.args.get('page', 1, type=int) # get the current page from URL
    per_page = 6

    brew_para = {
        "per_page": per_page,
        "page": page,
    }

    brew_response = requests.get(url=URL, params=brew_para)
    brew_response.raise_for_status()
    breweries = brew_response.json()

    # get total pages
    meta = requests.get('https://api.openbrewerydb.org/v1/breweries/meta').json()
    total = int(meta['total'])
    total_pages = (total + per_page - 1) // per_page

    return render_template("index.html", breweries=breweries, page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)