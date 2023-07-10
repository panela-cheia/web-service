from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

ingredients_unit_routes = Blueprint('ingredients-unit', __name__)

@ingredients_unit_routes.route('/ingredients-unit', methods=["POST"])
def create_ingredients():
    name = request.json['name']

    try:
        dive = Proxy("PYRONAME:adapters.create_ingredients_unit_adapter").execute(
            name=name)
        return jsonify({"create_ingredients" : dive}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredients_unit_routes.route('/delete_ingredients/<ingredients_unit_id>', methods=["DELETE"])
def delete_ingredients_unit(ingredients_unit_id):
    try:
        dive = Proxy("PYRONAME:adapters.delete_ingredients_unit_adapter").execute(
            id=ingredients_unit_id)
        return jsonify({"delete_ingredients_unit" : dive}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@ingredients_unit_routes.route('/list_ingredients_unit', methods=["GET"])
def list_ingredients_unit():
    try:
        dive = Proxy("PYRONAME:adapters.list_ingredients_unit_adapter").execute()
        return jsonify({"list_ingredients_unit" : dive}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500