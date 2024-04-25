from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db
from routers import get_users, get_user, create_user, update_user, delete_user

from werkzeug.security import check_password_hash
from models import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

# Registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)  # Default to False if not provided

    # Check if all required fields are provided
    if not first_name or not last_name or not email or not username or not password:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if the email or username already exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'Email or username already exists'}), 400

    # Create a new user
    new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, is_admin=is_admin)
    new_user.set_password(password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Sign-in route
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404


    if user.check_password(password):

        return jsonify({'message': 'Sign-in successful'}), 200
    else:
        return jsonify({'error': 'Incorrect password'}), 401


@app.route('/users', methods=['GET'])
def users():
    return get_users()

@app.route('/users/<email>', methods=['GET'])
def user(email):
    return get_user(email)

@app.route('/users', methods=['POST'])
def new_user():
    data = request.get_json()
    return create_user(data)

@app.route('/users/<email>', methods=['PUT'])
def edit_user(email):
    data = request.get_json()
    return update_user(email, data)

@app.route('/users/<email>', methods=['DELETE'])
def delete(email):
    return delete_user(email)

if __name__ == '__main__':
    app.run(debug=True)
