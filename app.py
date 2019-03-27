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
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(user.id))
    cartitems = ('Cart_item', backref='cart', lazy = True)

    def __init__(self, qty, total, user_id):
        self.qty = qty
        self.total = total
        self.user_id = user_id

# Routes go here

#post
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
#get

@app.route('/carts', methods=['GET'])
def return_carts():
    all_carts = db.session.query(Cart.id, Cart.qty, Cart.total, Cart.user_id).all()
    return jsonify(all_carts)

@app.route('/cart/<id>', methods=['GET'])
def return_single_cart(id):
    one_cart = db.session.query(Cart.id, Cart.qty, Cart.total, Cart.user_id).filter(Cart.id == id).first()
    return jsonify(one_cart)


#delete

@app.route('/cart/delete/<id>', methods=["DELETE"])
def cart_delete(id):
    if request.content_type == 'application/json':
       
        record = db.session.query(Cart).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("Completed Delete action")
    return jsonify("delete failed")


if __name__ == "__main__":
    app.debug = True
    app.run()