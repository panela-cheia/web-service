import os
import json
import requests

import openai

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from botocore.exceptions import BotoCoreError
from Pyro5.api import Proxy

from config.app import PORT
from config.swagger import SWAGGER_URL, SWAGGERUI_BLUEPRINT

from utils.files.generate_random_filename import generate_random_filename
from utils.files.upload_local import upload_local

from shared.infra.aws.S3 import s3

from shared.infra.http.routes.barn_routes import barn_routes
from shared.infra.http.routes.dive_routes import dives_routes
from shared.infra.http.routes.ingredients_unit_routes import ingredients_unit_routes
from shared.infra.http.routes.recipes_routes import recipes_routes
from shared.infra.http.routes.search_routes import search_routes
from shared.infra.http.routes.users_routes import users_routes

load_dotenv('.env')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp/uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png', 'gif'])

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)

@app.route('/files',methods=["POST"])
def create_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = generate_random_filename(secure_filename(file.filename))
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')
    file_url = None

    if upload_option == 'local':
        file_url = upload_local(file=file, filename=filename,app=app)
    elif upload_option == 's3':
        s3.upload(file, filename)
        file_url = s3.file_url(filename)
    else:
        return jsonify({'error': 'Invalid upload option'}), 400

    proxy_response = Proxy("PYRONAME:adapters.create_file_adapter").execute(name=filename,path=file_url)

    return jsonify(proxy_response), 201

@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file = Proxy("PYRONAME:adapters.find_file_by_name_adapter").execute(filename=filename)
    
    # Verifique o valor de UPLOAD_CONFIG_DEVELOPMENT para determinar o local de upload
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')

    if upload_option == 'local':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return '', 204
        else:
            return jsonify({'error': 'File not found'}), 404

    elif upload_option == 's3':
        try:
            s3.delete(filename=filename)

            proxy_response = Proxy("PYRONAME:adapters.delete_file_adapter").execute(id=file["id"])
            print(proxy_response)

            return '', 204
        except BotoCoreError as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid upload option'}), 400

# obs: lembrar sempre de usar o metodo com upload_option == 's3' 
@app.route('/files/classifiers', methods=['POST'])
def classifier_post_ai():
    try:
        file_url = request.args.get("file_url")

        api_key = os.getenv('SPOONACULAR_API_KEY')

        response = requests.get(
            f'https://api.spoonacular.com/food/images/classify?apiKey={api_key}&imageUrl={file_url}',
        )

        data = json.loads(response.__dict__['_content'].decode('utf-8'))
        print(data)

        # Acessar os campos desejados
        category = data['category']
        probability = data['probability']

        data_response = {
            category,
            probability
        }

        prompt = "Com base nos dados fornecidos pela API do spoonacular,"
        prompt += "Informe qual é a possível receita do usuário,Informe em portugues o nome da receita (traduza o nome se vindo de outra lingua) e em qual categoria se enquadra"
        prompt += f"Os dados são: {data_response}"

        # Parâmetros para a chamada da API do ChatGPT
        params = {
            'engine': 'text-davinci-003',
            'prompt': prompt,
            'max_tokens': 1000,  # Defina o número máximo de tokens na resposta
            # Controla a aleatoriedade das respostas (0.2 é mais determinístico, 0.8 é mais criativo)
            'temperature': 0.1,
            'n': 1,  # Gere apenas uma resposta
            'stop': None  # Não defina uma palavra de parada para a resposta
        }

        openai.api_key = os.getenv('OPENAI_KEY')
        # Fazendo a chamada para a API do ChatGPT
        response_open_api = openai.Completion.create(**params)

        # Obtendo a descrição gerada
        recipe = response_open_api.choices[0].text.strip()

        return jsonify({'description': recipe,
                        'category': category,
                        'probability': probability
                    }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/list', methods=['GET'])
def list_files_in_bucket():
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')
    
    if upload_option == 's3':
        response = s3.list_objs()

        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                file_url = s3.file_url(file_key)
                files.append({'key': file_key, 'url': file_url})

        return files
    elif upload_option == 'local':
        upload_folder = app.config['UPLOAD_FOLDER']
        file_names = os.listdir(upload_folder)
        files = []

        for file_name in file_names:
            if file_name == '.gitkeep':
                continue  # Ignorar o arquivo .gitkeep

            file_path = os.path.join(upload_folder, file_name)
            file_url = f'{request.host_url}files/{file_name}'
            files.append({'name': file_name, 'url': file_url})

        return jsonify(files)

    else:
        return jsonify({'error': 'Invalid upload option'}), 400
    
@app.route('/')
def index():
    return jsonify({'ok': 'api is running! Time to cooking 🥘'}), 200


# Register barn routes
app.register_blueprint(barn_routes)

# Register dives routes
app.register_blueprint(dives_routes)

# Register ingredients unit routes
app.register_blueprint(ingredients_unit_routes)

# Register recipes routes
app.register_blueprint(recipes_routes)

# Register search routes
app.register_blueprint(search_routes)

# Register users routes
app.register_blueprint(users_routes)

if __name__ == '__main__':

    # Adicione a blueprint do Swagger ao aplicativo
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.run(port=PORT, debug=True)