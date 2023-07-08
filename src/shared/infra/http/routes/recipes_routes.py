from flask import Blueprint, jsonify
# from Pyro5.api import Proxy

recipes_routes = Blueprint('recipes', __name__)

@recipes_routes.route('/recipes', methods=["GET"])
def example():
    return jsonify({'ok': 'recipes routes'}), 200