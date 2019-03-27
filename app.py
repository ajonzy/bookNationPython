from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mtzexrunaysute:87ff40992391ec6a4d3519c55741332fdf4017d09f9c2675b56d0fcdf86e03ea@ec2-54-225-129-101.compute-1.amazonaws.com:5432/da35vkc3i6vgao"

heroku = Heroku(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Classes go here
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    spanish_title = db.Column(db.String(40), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    spanish_genre = db.Column(db.String(40), nullable=False)
    summary = db.Column(db.String(5000), nullable=False)
    spanish_summary = db.Column(db.String(5000), nullable=False)
    cart_item = db.relationship('Cart_item', backref='book', lazy=True)

    def __init__ (self, title, spanish_title, author, cost, genre, spanish_genre, summary, spanish_summary, cart_item):
        self.title = title
        self.spanish_title = spanish_title
        self.author = author
        self.cost = cost
        self.genre = genre
        self.spanish_genre = spanish_genre
        self.summary = summary
        self.spanish_summary = spanish_summary
        self.cart_item = cart_item


    

# Routes go here


if __name__ == "__main__":
    app.debug = True
    app.run()