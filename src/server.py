import os
import random
import string
import json

import openai
import boto3

import requests

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from botocore.exceptions import BotoCoreError


from config.app import PORT
from config.swagger import SWAGGER_URL,SWAGGERUI_BLUEPRINT

load_dotenv('.env')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp/uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png', 'gif'])

def generate_random_filename(filename):
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))
    name, ext = os.path.splitext(filename)
    random_filename = f'{random_string}-{name}{ext}'
    return random_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


def upload_local(file, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    base_url = os.getenv('BASE_URL')
    file_url = f'{base_url}/files/{filename}'
    return file_url


def upload_s3(file, filename):
    s3_bucket = os.getenv('S3_BUCKET_NAME')
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(file, s3_bucket, filename)
    file_url = f'https://{s3_bucket}.s3.amazonaws.com/{filename}'
    return file_url

@app.route('/posts', methods=['POST'])
def create_post():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = generate_random_filename(secure_filename(file.filename))
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')
    file_url = None

    if upload_option == 'local':
        file_url = upload_local(file, filename)
    elif upload_option == 's3':
        file_url = upload_s3(file, filename)
    else:
        return jsonify({'error': 'Invalid upload option'}), 400

    # Implement your logic to create a post in the database
    post = {
        'name': filename,
        'url': file_url
    }

    return jsonify(post), 201

@app.route('/posts/<filename>', methods=['DELETE'])
def delete_file(filename):
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
        s3_bucket = os.getenv('S3_BUCKET_NAME')
        s3_client = boto3.client('s3')
        try:
            s3_client.delete_object(Bucket=s3_bucket, Key=filename)
            return '', 204
        except BotoCoreError as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid upload option'}), 400

@app.route('/posts', methods=['GET'])
def list_files_in_bucket():
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')
    if upload_option == 's3':
        s3_bucket = os.getenv('S3_BUCKET_NAME')
        s3_client = boto3.client('s3')
        response = s3_client.list_objects_v2(Bucket=s3_bucket)

        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                file_url = f'https://{s3_bucket}.s3.amazonaws.com/{file_key}'
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


@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)


@app.route('/')
def index():
    return jsonify({'ok': 'api is running!'}), 200


@app.route("/recipes/description", methods=['POST'])
def description_recipe():
    # Verificar se o corpo da solicitação contém o nome da receita
    if 'name' not in request.json:
        return jsonify({'error': 'Name of the recipe is required.'}), 400

    # Obter o nome da receita a partir do corpo da solicitação
    nome_receita = request.json['name']

    # Prompt inicial para a geração de descrição da receita
    prompt = f"Aqui está uma descrição da receita de {nome_receita} com no máximo 40 caracteres, querendo convencer outras pessoas a fazerem a receita:"

    # Parâmetros para a chamada da API do ChatGPT
    params = {
        'engine': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 40,  # Defina o número máximo de tokens na resposta
        # Controla a aleatoriedade das respostas (0.2 é mais determinístico, 0.8 é mais criativo)
        'temperature': 0.8,
        'n': 1,  # Gere apenas uma resposta
        'stop': None  # Não defina uma palavra de parada para a resposta
    }

    try:
        openai.api_key = os.getenv('OPENAI_KEY')
        # Fazendo a chamada para a API do ChatGPT
        response = openai.Completion.create(**params)

        # Obtendo a descrição gerada
        descricao = response.choices[0].text.strip()

        return jsonify({'description': descricao}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/recipes/ingredients", methods=['POST'])
def ingredients_recipe():
    # Verificar se o corpo da solicitação contém o nome da receita
    if 'name' not in request.json:
        return jsonify({'error': 'Name of the recipe is required.'}), 400
    if 'description' not in request.json:
        return jsonify({'error': 'Name of the recipe is required.'}), 400

    # Obter o nome da receita a partir do corpo da solicitação
    nome_receita = request.json['name']
    descricao_receita = request.json['description']

    prompt = f"Sendo uma receita culinária de nome {nome_receita}, com a seguinte descrição: '{descricao_receita}',"
    prompt += "informe a lista de ingredientes possíveis da receita\n. Cada ingrediente é uma tripla com os campos:"
    prompt += "'name' (String), 'amount' (Integer) e 'unit' (String).\n"
    prompt += "A lista de unidades possíveis é a seguinte:\n\n"
    prompt += "['Unidade','Miligrama (mg)','Copo','Fio','Grama (g)','Pitada','Litro (l)','Raspas',"
    prompt += "'Tablete','Ramo','Colher de chá (c.c.)','Mililitro (ml)','Xícara (xíc.)',"
    prompt += "'Filete','Colher de sopa (c.s.)','Quilograma (kg)','Punhado']."
    prompt += "Retorne a lista de ingredientes como uma string JSON contendo em cada objeto os campos 'name', 'amount' e 'unit'."
    prompt += "Certifique-se de que a string JSON esteja corretamente formatada, com cada objeto de ingredientes separado por vírgula e o array de ingredientes devidamente fechado com colchetes no final."
    # Parâmetros para a chamada da API do ChatGPT
    params = {
        'engine': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 400,  # Defina o número máximo de tokens na resposta
        # Controla a aleatoriedade das respostas (0.2 é mais determinístico, 0.8 é mais criativo)
        'temperature': 0.1,
        'n': 1,  # Gere apenas uma resposta
        'stop': None  # Não defina uma palavra de parada para a resposta
    }

    try:

        openai.api_key = os.getenv('OPENAI_KEY')
        # Fazendo a chamada para a API do ChatGPT
        response = openai.Completion.create(**params)

        # Obtendo a descrição gerada
        ingredients = response.choices[0].text.strip()

        ingredients_json = json.loads(ingredients)

        return jsonify({'ingredients': ingredients_json}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/posts/classifier', methods=['POST'])
def create_post_ai():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = generate_random_filename(secure_filename(file.filename))
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')
    file_url = None

    if upload_option == 'local':
        file_url = upload_local(file, filename)
    elif upload_option == 's3':
        file_url = upload_s3(file, filename)
    else:
        return jsonify({'error': 'Invalid upload option'}), 400

    api_key = os.getenv('SPOONACULAR_API_KEY')
    
    response = requests.get(
        f'https://api.spoonacular.com/food/images/classify?apiKey={api_key}&imageUrl={file_url}',
    )

    data = json.loads(response.__dict__['_content'].decode('utf-8'))

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

    return jsonify({ 'description':recipe,
        'category':category,
        'probability':probability}), 201

if __name__ == '__main__':

    # Adicione a blueprint do Swagger ao aplicativo
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.run(port=PORT, debug=True)