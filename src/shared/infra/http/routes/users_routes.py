from flask import Blueprint, jsonify
# from Pyro5.api import Proxy

users_routes = Blueprint('users', __name__)

@users_routes.route('/users', methods=["GET"])
def example():
    return jsonify({'ok': 'users routes'}), 200