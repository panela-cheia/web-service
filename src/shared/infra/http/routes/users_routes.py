from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

users_routes = Blueprint('users', __name__)

@users_routes.route('/users', methods=["POST"])
def create_user():
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    try:
        user = Proxy("PYRONAME:adapters.create_user_adapter").execute(
            name=name,
            username=username,
            email=email,
            password=password
        )

        return jsonify({'data': user}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@users_routes.route('/users/login', methods=["POST"])
def auth():
    email = request.json["email"]
    password = request.json["password"]

    try:
        user = Proxy("PYRONAME:adapters.user_login_adapter").execute(
            email=email,
            password=password
        )

        return jsonify({'data': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@users_routes.route('/users/login-username', methods=["POST"])
def auth_username():
    username = request.json["username"]
    password = request.json["password"]

    try:
        user = Proxy("PYRONAME:adapters.login_user_with_username_adapter").execute(
            username=username,
            password=password
        )

        return jsonify({'data': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@users_routes.route('/users/follow', methods=["POST"])
def follow():
    user_id = request.json["userId"]
    follow_id = request.json["followId"]

    try:
        user = Proxy("PYRONAME:adapters.follow_user_adapter").execute(
            user_id=user_id,
            follow_id=follow_id
        )

        return jsonify({'data': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@users_routes.route('/users/unfollow', methods=["POST"])
def unfollow():
    user_id = request.json["userId"]
    unfollow_id = request.json["unfollowId"]

    try:
        user = Proxy("PYRONAME:adapters.unfollow_user_adapter").execute(
            user_id=user_id,
            unfollow_id=unfollow_id
        )

        return jsonify({'data': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@users_routes.route('/users/all', methods=["GET"])
def listAll():
    try:
        data = Proxy("PYRONAME:adapters.list_all_users_adapters").execute()

        return jsonify({'data': data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@users_routes.route('/users/<id>/others', methods=["GET"])
def listOthers(id):
    try:
        data = Proxy("PYRONAME:adapters.list_others_users_adapter").execute(id=id)

        return jsonify({'data': data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_routes.route('/users/search_barn', methods=["GET"])
def search_in_users_barn():
    user_id = request.args.get("user")
    value = request.args.get("value")
    
    try:
        search_user = Proxy("PYRONAME:adapters.search_in_users_barn_adapter").execute(
            user_id=user_id,
            value=value
        )

        return jsonify({'search_result': search_user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_routes.route('/users/search', methods=["GET"])
def search():
    user_id = request.args.get("user")
    value = request.args.get("value")
    
    try:
        search_user = Proxy("PYRONAME:adapters.search_users_adapter").execute(
            user_id=user_id,
            value=value
        )

        return jsonify({'search_result': search_user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_routes.route('/users/<id>/update_profile', methods=["PUT"])
def update_user(id):
    name = request.json["name"]
    bio = request.json["bio"]
    username = request.json["username"]
    
    try:
        user = Proxy("PYRONAME:adapters.update_user_adapter").execute(
            id=id,
            name=name,
            bio=bio,
            username=username
        )
    
        return jsonify({'user':user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500