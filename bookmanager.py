import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file #database store

db = SQLAlchemy(app) #initilise the database
class Book(db.Model): #basic class inherit from basic database model, which will used to store  book objects
    title = db.Column(db.String(80), unique=True, nullable=True, primary_key=True)
    rating = db.Column(db.Integer(), unique=False, nullable=True, primary_key=False)

    def __repr__(self): #to represent book object as an string
        return "<Title: {}  Rating: {}>".format(self.title ,self.rating)


@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            print("adding new book:")
            print("title : "+request.form.get("title"))
            print("rating : "+request.form.get("rating"))
            book = Book(title=request.form.get("title"),rating=request.form.get("rating") )
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            db.session.rollback()
            print(e)
    print("finding all books from db:")
    books = Book.query.all()
    print(books)
    return render_template("home.html", books=books)
    print(Book.query.all())

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title = oldtitle).first()
        book.title = newtitle
        db.session.commit()
     
    except Exception as e:
        print("Couldn't update book title")
        db.session.rollback()
        print(e)
    return redirect("/")
@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    