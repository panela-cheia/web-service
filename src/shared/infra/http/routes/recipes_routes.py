from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

recipes_routes = Blueprint('recipes', __name__)

@recipes_routes.route('/recipes', methods=["POST"])
def create_recipe():
    name = request.json["name"]
    description = request.json["description"]
    ingredients = request.json["ingredients"]
    userId = request.json["userId"]
    fileId = request.json["fileId"]
    diveId = request.json["diveId"]

    try:
        recipe = Proxy("PYRONAME:adapters.create_recipe_adapter").execute(
            name=name,
            description=description,
            ingredients=ingredients,
            userId=userId,
            fileId=fileId,
            diveId=diveId
        )

        return jsonify({'data': recipe}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@recipes_routes.route('/recipes', methods=["GET"])
def list_recipes():
    try:
        recipes = Proxy("PYRONAME:adapters.list_recipe_adapter").execute()

        return jsonify({'data': recipes}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500