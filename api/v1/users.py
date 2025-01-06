from flask import Blueprint, jsonify, abort, request
from sqlalchemy.exc import IntegrityError

users_api = Blueprint('users_api', __name__, url_prefix='/api/v1')


@users_api.route('/users', methods=["GET"], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all user objects
    """
    from api.views.db import Users
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])

@users_api.route('/user/new/', methods=['POST'], strict_slashes=False)
def new_user():
    '''Creates a new user'''
    from api.views.db import  Users
    from app import db
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    if "username" not in data:
        return jsonify({"error": "Missing username"}), 400
    
    try:
        new_user = Users(username=data.get("username"), email=data.get("email"))
        new_user.set_password(data.get("password"))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    
    except IntegrityError as e:
        return jsonify({"Error": str(e.orig)})
        if 'users_email_key' in str(e.orig):
            return jsonify({"error": "Email already exists"}), 400
        elif 'users_username_key' in str(e.orig):
            return jsonify({"error": "Username already exists"}), 400
        else:
            return jsonify({"error": "An error occurred while creating the user"}), 500