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
    cart = db.relationship('Cart', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cart_items = db.relationship('Cart_item', backref='cart', lazy = True)


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
    cart_items = db.relationship('Cart_item', backref='book', lazy=True)
    order_items = db.relationship('Order_item', backref='book', lazy=True)
    
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
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    
    def __init__(self, cart_id, book_id):
      self.cart_id = cart_id
      self.book_id = book_id

# Order
class Order(db.Model):
    __tablename__ ="order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_items = db.relationship('Order_item', backref='order', lazy=True)
    

    def __init__(self, user_id, date, total):
        self.user_id = user_id
        self.date = date
        self.total = total


class Order_item(db.Model):
    __tablename__ ="order_item"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    

    def __init__(self, order_id, book_id):
        self.order_id = order_id
        self.book_id = book_id



# Routes go here
@app.route('/library', methods=['GET'])
def return_library():
    all_books = db.session.query(Book.id, Book.title, Book.spanish_title, Book.author, Book.cost, Book.cover_url, Book.genre, Book.spanish_genre, Book.summary, Book.spanish_summary).all()
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
    book = db.session.query(Book.title, Book.spanish_title, Book.author, Book.cost, Book.cover_url, Book.genre, Book.spanish_genre, Book.summary, Book.spanish_summary).filter(Book.id == id).first()
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
        user_type = 'user'
        genre_preferences = post_data.get('genre_preferences')
        
        reg = User(name, email, password, user_type, genre_preferences)
        db.session.add(reg)
        db.session.commit()

        qty = 0
        total = 0
        record = Cart(qty, total)
        db.session.add(record)
        db.session.commit()
        return jsonify("User Posted")
    return jsonify("Something went wrong")

@app.route('/users', methods=['GET'])
def return_all_users():
    all_users = db.session.query(User.id, User.name, User.email, User.password, User.user_type, User.genre_preferences).all()
    return jsonify(all_users)

@app.route("/users/verification", methods=["POST"])
def user_verification():
    if request.content_type == "application/json":
        post_data = request.get_json()
        user_password = post_data.get("password")
        check_email = db.session.query(User.email).filter(User.email == post_data.get("email")).first()
        if check_email is None:
            return jsonify("User NOT Verified")
        valid_password = db.session.query(User.password).filter(User.email == post_data.get("email")).first()[0]
        if valid_password is None:
            return jsonify("User NOT Verified")
        if user_password != valid_password:
            return jsonify("User NOT Verified")
        return jsonify("User Verified")
    return jsonify("Error verifying user")


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

@app.route("/cart/user/<user_id>", methods=["GET"])
def return_cart_by_user(user_id):
    one_cart = db.session.query(Cart.id, Cart.qty, Cart.total).filter(Cart.user_id == user_id).first()
    return jsonify(one_cart)

@app.route("/cart_items/cart/<cart_id>")
def get_cart_items_by_cart(cart_id):
    cart_items = db.session.query(Cart_item.book_id).filter(Cart_item.cart_id == cart_id).all()
    return jsonify(cart_items)

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

@app.route('/single/user/<id>', methods=["GET"])
def return_single_user(id):
    single_user = db.session.query(User.id, User.name, User.email, User.password, User.user_type, User.genre_preferences).filter(User.id == id).first()
    return jsonify(single_user)

@app.route('/single/email/user/<email>', methods=["GET"])
def return_single_user_by_email(email):
    single_user_by_email = db.session.query(User.id, User.name, User.email, User.password, User.user_type, User.genre_preferences).filter(User.email == email).first()
    return jsonify(single_user_by_email)


# Order Routes
@app.route('/order/input', methods = ['POST'])
def order_input():
    if request.content_type == 'application/json':
       post_data = request.get_json()
       user_id = post_data.get("user_id")
       date = post_data.get('date')
       total = post_data.get('total')
       rec = Order(user_id, date, total)
       db.session.add(rec)    
       db.session.commit()
       return jsonify("Order Posted")
    return jsonify('Something went wrong')


@app.route('/orders', methods=['GET'])
def return_orders():
    all_orders = db.session.query(Order.id, Order.user_id, Order.date, Order.total).all()
    return jsonify(all_orders)


@app.route('/delete/order/<id>', methods=["DELETE"])
def order_delete(id):
    record = db.session.query(Order).get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify('Completed delete Order')


@app.route('/search/<title>', methods=['GET'])
def book_search(title):
    print(title)
    search_book = db.session.query(Book.id, Book.title, Book.spanish_title, Book.author, Book.cost, Book.genre, Book.spanish_genre, Book.summary, Book.spanish_summary ).filter(Book.title == (title.title())).first()
    print(search_book)
    return jsonify(search_book)

  

if __name__ == "__main__":
    app.debug = True
    app.run()