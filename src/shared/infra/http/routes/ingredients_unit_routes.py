from flask import Blueprint, jsonify
# from Pyro5.api import Proxy

ingredients_unit_routes = Blueprint('ingredients-unit', __name__)

@ingredients_unit_routes.route('/ingredients-unit', methods=["GET"])
def list_ingredients_unit():
    return jsonify({'ok': 'Ingredients Unit'}), 200