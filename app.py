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
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    spanish_title = db.Column(db.String(180), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    spanish_genre = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    spanish_summary = db.Column(db.String(), nullable=False)
    # cart_items = db.relationship('Cart_item', backref='book', lazy=True)
    # order_items = db.relationship('Order_item', backref='book', lazy=True)

    def __init__ (self, title, spanish_title, author, cost, genre, spanish_genre, summary, spanish_summary):
        self.title = title
        self.spanish_title = spanish_title
        self.author = author
        self.cost = cost
        self.genre = genre
        self.spanish_genre = spanish_genre
        self.summary = summary
        self.spanish_summary = spanish_summary


    

# Routes go here
@app.route('/library', methods=['GET'])
def return_library():
    all_books = db.session.query(Book.id, Book.title, Book.spanish_title, Book.author, Book.cost, Book.genre, Book.spanish_genre, Book.summary, Book.spanish_summary).all()
    return jsonify(all_books)

@app.route('/library/input', methods=['POST'])
def input_book():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        spanish_title = post_data.get('spanish_title')
        author = post_data.get('author')
        cost = post_data.get('cost')
        genre = post_data.get('genre')
        spanish_genre = post_data.get('spanish_genre')
        summary = post_data.get('summary')
        spanish_summary = post_data.get('spanish_summary')
        record = Book(title, spanish_title, author, cost, genre, spanish_genre, summary, spanish_summary)
        db.session.add(record)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("Error adding Book")

@app.route('/library/<id>', methods=["GET"])
def return_book(id):
    book = db.session.query(Book.title, Book.spanish_title, Book.author, Book.cost, Book.genre, Book.spanish_genre, Book.summary, Book.spanish_summary).filter(Book.id == id).first()
    return jsonify(book)

@app.route('/library/delete/<id>', methods=["DELETE"])
def delete_book(id):
    book = db.session.query(Book).get(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify("Completed Delete action")



if __name__ == "__main__":
    app.debug = True
    app.run()