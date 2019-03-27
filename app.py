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
    orders = db.relationship('Orders', backref='user', lazy=True)


    def __init__(self, name, email, password, user_type, genre_preferences):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.genre_preferences = genre_preferences

    def __repr__(self):
        return '<Title %r>' % self.title


# Routes go here
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



@app.route('/delete/user/<id>', methods=["DELETE"])
def user_delete(id):
    record = db.session.query(User).get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify('Completed delete user')




if __name__ == "__main__":
    app.debug = True
    app.run()