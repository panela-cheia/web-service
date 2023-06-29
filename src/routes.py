from flask import Blueprint

from posts_routes import post_routes

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return 'Hello, world!'


# Importe as rotas auxiliares e registre-as no blueprint
routes.register_blueprint(post_routes)