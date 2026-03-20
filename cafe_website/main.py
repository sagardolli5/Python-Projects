from flask import Flask,render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.utils import redirect

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    location = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    hours = db.Column(db.String(100))
    reservation_hours = db.Column(db.String(100))
    photo_url = db.Column(db.String(300))
    description = db.Column(db.Text)
    has_wifi          = db.Column(db.Boolean, default=False)
    has_toilet        = db.Column(db.Boolean, default=False)
    has_parking       = db.Column(db.Boolean, default=False)
    has_sockets       = db.Column(db.Boolean, default=False)
    can_take_calls    = db.Column(db.Boolean, default=False)
    seats_available   = db.Column(db.Integer, default=0)
    coffee_prices     = db.Column(db.String(300))


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    search = request.args.get('search', '').strip()
    if search:
        all_cafes = Cafe.query.filter(
            Cafe.name.ilike(f'%{search}%') |
            Cafe.location.ilike(f'%{search}%') |
            Cafe.category.ilike(f'%{search}%')
        ).all()
    else:
        all_cafes = Cafe.query.all()
    return render_template('index.html', all_cafes=all_cafes, cafe_count=len(all_cafes))

@app.route("/cafe/<int:cafe_id>")
def cafe_detail(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return render_template("detail.html", cafe=cafe)

@app.route("/new_cafe", methods=["GET","POST"])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get('name'),
            category=request.form.get('category'),
            location=request.form.get('location'),
            phone=request.form.get('phone'),
            hours=request.form.get('hours'),
            reservation_hours=request.form.get('reservation_hours'),
            photo_url=request.form.get('photo_url'),
            description=request.form.get('description'),
            has_wifi=bool(request.form.get('has_wifi')),
            has_toilet=bool(request.form.get('has_toilet')),
            has_parking=bool(request.form.get('has_parking')),
            has_sockets=bool(request.form.get('has_sockets')),
            can_take_calls=bool(request.form.get('can_take_calls')),
            seats_available=int(request.form.get('seats_available') or 0),
            coffee_prices=request.form.get('coffee_prices'),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return render_template('success.html', cafe=new_cafe)
    return render_template("new_cafe.html")

@app.route("/confirm/<int:cafe_id>")
def confirm_delete(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    return render_template("confirm.html", cafe=cafe)

@app.route("/delete/<int:cafe_id>", methods=["POST"])
def delete(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/direction/<int:cafe_id>")
def direction(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    return render_template("directions.html", cafe=cafe)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
