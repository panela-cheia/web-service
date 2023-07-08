from flask import Blueprint, jsonify
# from Pyro5.api import Proxy

dives_routes = Blueprint('dives', __name__)

@dives_routes.route('/dives', methods=["GET"])
def list_ingredients_unit():
    return jsonify({'ok': 'dives routes'}), 200