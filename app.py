from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from .models import db
from .routes import get_users, get_user, create_user, update_user, delete_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
    db.create_all()
    app.run(debug=True)
