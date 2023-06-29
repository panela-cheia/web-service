import os
import random
import string

from flask import Flask, request, jsonify, send_from_directory,Response
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
import boto3

from botocore.exceptions import BotoCoreError

import openai
import json

import requests

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
    
@app.route("/emails", methods=['POST'])
def send_email():
    try:
            # Endpoint da API para envio de e-mails
        endpoint = os.getenv('MAILGUN_BASE_URL') + "/messages"

        # Parâmetros da requisição
        params = {
            'from': "Excited User luciano.alcantara@ufv.br",
            'to': ["vinicius.o.mendes@ufv.br"],
            'subject': "Hello",
            'text': "Testing some Mailgun awesomeness!"
        }

        # Autenticação com a chave de API do Mailgun
        auth = ('api', os.getenv('MAILGUN_API_KEY'))

        # Enviar a requisição POST para a API do Mailgun
        response = requests.post(endpoint, auth=auth, data=params)

        # Verificar o status da resposta
        if response.status_code == 200:
            print('E-mail enviado com sucesso!')
        else:
            print('Erro ao enviar o e-mail.')
            print(response.text)

        return jsonify({'ok': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
       

if __name__ == '__main__':
    app.run(port=3333, debug=True)