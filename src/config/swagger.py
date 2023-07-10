from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL da interface do Swagger
API_URL = '/static/swagger.json'  # URL do arquivo swagger.json

# Configuração do Swagger
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Panela Cheia API"  # Nome do seu aplicativo
    }
)
