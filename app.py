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

class User(db.Model):
    __tablename__ ="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(), nullable=False)
    user_type = db.Column(db.String(80), nullable=False)
    genre_preferences = db.Column(db.String(80), nullable=True)
    # cart = db.relationship('Cart', backref='user', lazy=True)
    # orders = db.relationship('Orders', backref='user', lazy=True)

    def __init__(self, name, email, password, user_type, genre_preferences):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.genre_preferences = genre_preferences

    def __repr__(self):
        return '<Title %r>' % self.title


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # cart_items = db.relationship('Cart_item', backref='cart', lazy = True)

    def __init__(self, qty, total, user_id):
        self.qty = qty
        self.total = total
        self.user_id = user_id

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    spanish_title = db.Column(db.String(180), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    cover_url = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    spanish_genre = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    spanish_summary = db.Column(db.String(), nullable=False)
    # cart_items = db.relationship('Cart_item', backref='book', lazy=True)
    # order_items = db.relationship('Order_item', backref='book', lazy=True)
    
    def __init__ (self, title, spanish_title, author, cost, cover_url, genre, spanish_genre, summary, spanish_summary):
        self.title = title
        self.spanish_title = spanish_title
        self.author = author
        self.cost = cost
        self.cover_url = cover_url
        self.genre = genre
        self.spanish_genre = spanish_genre
        self.summary = summary
        self.spanish_summary = spanish_summary
    
    def __repr__(self):
        return '<Title %r>' % self.title



class Cart_item(db.Model):
    __tablename__="cart_item"
    id = db.Column(db.Integer, primary_key=True)
    # cart_id = db.Column(db.Integer, db.ForeignKey(Cart.id))
    # book_id = db.Column(db.Integer, db.ForeignKey(Book.id))

    def __repr__(self):
        return '<Title %r>' % self.title
    

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
        cover_url = post_data.get('cover_url')
        genre = post_data.get('genre')
        spanish_genre = post_data.get('spanish_genre')
        summary = post_data.get('summary')
        spanish_summary = post_data.get('spanish_summary')
        record = Book(title, spanish_title, author, cost, cover_url, genre, spanish_genre, summary, spanish_summary)
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

@app.route('/user/input', methods=['POST'])
def user_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()

        name = post_data.get('name')
        email = post_data.get('email')
        password = post_data.get('password')
        user_type = post_data.get('user_type')
        genre_preferences = post_data.get('genre_preferences')
        
        reg = User(name, email, password, user_type, genre_preferences)
        db.session.add(reg)
        db.session.commit()
        return jsonify("User Posted")
    return jsonify("Something went wrong")

@app.route('/users', methods=['GET'])
def return_all_users():
    all_users = db.session.query(User.id, User.name, User.email, User.password, User.user_type, User.genre_preferences).all()
    return jsonify(all_users)


@app.route('/cart/input', methods = ['POST'])
def cart_input():
    if request.content_type == 'application/json':
       post_data = request.get_json()
       qty = post_data.get('qty')
       total = post_data.get('total')
       user_id = post_data.get("user_id")
       rec = Cart(qty, total)
       db.session.add(rec)    
       db.session.commit()
       return jsonify("Data Posted")

    return jsonify('Something went wrong')

@app.route('/carts', methods=['GET'])
def return_carts():
    all_carts = db.session.query(Cart.id, Cart.qty, Cart.total, Cart.user_id).all()
    return jsonify(all_carts)

@app.route('/cart/<id>', methods=['GET'])
def return_single_cart(id):
    one_cart = db.session.query(Cart.id, Cart.qty, Cart.total, Cart.user_id).filter(Cart.id == id).first()
    return jsonify(one_cart)

@app.route('/cart/delete/<id>', methods=["DELETE"])
def cart_delete(id):
    if request.content_type == 'application/json':
       
        record = db.session.query(Cart).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("Completed Delete action")
    return jsonify("delete failed")

@app.route('/user/delete/<id>', methods=["DELETE"])
def user_delete(id):
    record = db.session.query(User).get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify('Completed delete user')
  

if __name__ == "__main__":
    app.debug = True
    app.run()