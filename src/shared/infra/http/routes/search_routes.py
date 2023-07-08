from flask import Blueprint, jsonify
# from Pyro5.api import Proxy

search_routes = Blueprint('search-routes', __name__)

@search_routes.route('/search', methods=["GET"])
def example():
    return jsonify({'ok': 'search routes'}), 200