from flask import request, jsonify
from .models import User, db

def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

def get_user(email):
    user = User.query.get_or_404(email)
    return jsonify(user.to_dict()), 200

def create_user(data):
    new_user = User(email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    username=data['username'])
    new_user.set_password(data['password'])
    try:
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Email or username already exists'}, 400

def update_user(email, data):
    user = User.query.get_or_404(email)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('username', user.username)
    user.is_admin = data.get('is_admin', user.is_admin)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return {'message': 'User updated successfully'}, 200

def delete_user(email):
    user = User.query.get_or_404(email)
    db.session.delete(user)
    db.session.commit()
    return {'message': 'User deleted successfully'}, 200
