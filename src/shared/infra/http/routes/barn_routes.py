from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

barn_routes = Blueprint('barn', __name__)

@barn_routes.route('/barn/save', methods=["POST"])
def save_recipe():
    barnId = request.json["barnId"]
    recipeId = request.json["recipeId"]
    
    try:
        user = Proxy("PYRONAME:adapters.save_recipe_adapter").execute(
            barnId = barnId,
            recipeId = recipeId
        )
        
        return jsonify({'user': user}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@barn_routes.route('/barn/<barnId>/remove/<recipeId>', methods=["DELETE"])
def remove_recipe(barnId, recipeId):
    try:
        user = Proxy("PYRONAME:adapters.remove_recipe_adapter").execute(
            barnId = barnId,
            recipeId = recipeId
        )
        
        return jsonify({'user': user}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@barn_routes.route('/barn/search', methods=["GET"])
def search_recipe():
    barnId = request.args.get("barn")
    recipeName = request.args.get("recipe")
    
    try:
        user = Proxy("PYRONAME:adapters.search_recipe_barn_adapter").execute(
            barnId = barnId,
            recipeName = recipeName
        )
        
        return jsonify({'user': user}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500