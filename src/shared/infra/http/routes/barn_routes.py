from flask import Blueprint, jsonify
# from Pyro5.api import Proxy

barn_routes = Blueprint('barn', __name__)

@barn_routes.route('/barn', methods=["GET"])
def example():
    return jsonify({'ok': 'barn routes'}), 200