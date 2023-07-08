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
    
@recipes_routes.route('/recipes/<id>/react', methods=["PUT"])
def react(id):
    user_id = request.json["user_id"]
    typeR = request.json["type"]
    
    try:
        recipes = Proxy("PYRONAME:adapters.reaction_recipe_adapter").execute(
            recipe_id=id,
            user_id=user_id,
            type=typeR
        )

        return jsonify({'data': recipes}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@recipes_routes.route('/recipes/search', methods=["GET"])
def search():
    name = request.args.get("name")
    
    try:
        recipes = Proxy("PYRONAME:adapters.search_recipe_adapter").execute(
            name=name
        )

        return jsonify({'data': recipes}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500