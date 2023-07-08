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