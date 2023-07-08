from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

users_routes = Blueprint('users', __name__)

@users_routes.route('/users', methods=["POST"])
def create_user():
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    try:
        user = Proxy("PYRONAME:adapters.create_user_adapter").execute(
            name=name,
            username=username,
            email=email,
            password=password
        )

        return jsonify({'data': user}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@users_routes.route('/users/login', methods=["POST"])
def auth():
    email = request.json["email"]
    password = request.json["password"]

    try:
        user = Proxy("PYRONAME:adapters.user_login_adapter").execute(
            email=email,
            password=password
        )

        return jsonify({'data': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500