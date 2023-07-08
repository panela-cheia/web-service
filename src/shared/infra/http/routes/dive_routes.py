from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

dives_routes = Blueprint('dives', __name__)

@dives_routes.route('/dives', methods=["POST"])
def create_dive():
    name = request.json['name']
    description = request.json['description']
    fileId = request.json['fileId']
    userId = request.json['userId']

    try:
        dive = Proxy("PYRONAME:adapters.create_dive_adapter").execute(
            name=name, 
            description=description, 
            fileId=fileId, 
            userId=userId)
        return jsonify({"create_dive" : dive}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dives_routes.route('/dives/enter_dive', methods=["POST"])
def enter_dive():
    user_id = request.json['userId']
    dive_id = request.json['diveId']

    try:
        dive = Proxy("PYRONAME:adapters.enter_dive_adapter").execute(
            userId=user_id, 
            diveId=dive_id)
        return jsonify({"enter_dive" : dive}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@dives_routes.route('/dives/exit_dive', methods=["PUT"])
def exit_dive():
    user = request.json['userId']
    new_owner = request.json['new_owner']
    diveId = request.json['diveId']

    try:
        dive = Proxy("PYRONAME:adapters.exit_dive_adapter").execute(
            user=user,
            new_owner=new_owner if "new_owner" else None,
            diveId=diveId)
        return jsonify({"exit_dive" : dive}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dives_routes.route('/dives/list_dive_recipes/<dive_id>', methods=["GET"])
def list_dive_recipes(dive_id):
    try:
        dive = Proxy("PYRONAME:adapters.list_dive_recipes_adapter").execute(
            diveId=dive_id)
        return jsonify({"list_dive_recipes" : dive}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dives_routes.route('/dives/list_dives/<user_id>', methods=["GET"])
def list_dives(user_id):
    try:
        dive = Proxy("PYRONAME:adapters.list_users_adapter").execute(
            userId=user_id)
        return jsonify({"list_dives" : dive}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@dives_routes.route('/dives/search_dive/<diveName>', methods=["GET"])
def search_dive(diveName):
    try:
        dive = Proxy("PYRONAME:adapters.search_dive_adapter").execute(
            diveName=diveName)
        return jsonify({"search_dive" : dive}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dives_routes.route('/dives/update_dive', methods=["PUT"])
def update_dive():
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    fileId = request.json['fileId']

    try:
        dive = Proxy("PYRONAME:adapters.update_dive_adapter").execute(
            id=id,
            name=name,
            description=description,
            fileId=fileId,)
        return jsonify({"update_dive" : dive}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
