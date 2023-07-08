from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

search_routes = Blueprint('search', __name__)

@search_routes.route('/search', methods=["GET"])
def search_dive_and_users():
    search_value = request.args.get("value")
    user_id = request.args.get("user_id")
    
    try:
        user = Proxy("PYRONAME: adapters.search_dive_and_users_adapter").execute(
            search_value = search_value,
            user_id = user_id
        )
        
        return jsonify({'users': user}), 200
    
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500