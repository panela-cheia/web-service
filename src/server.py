import os
import random
import string

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
import boto3

from botocore.exceptions import BotoCoreError

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
    else:
        return jsonify({'error': 'upload file option is local!'}), 400

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)

@app.route('/')
def index():
    return jsonify({'ok': 'api is running!'}), 200


if __name__ == '__main__':
    app.run(port=3333, debug=True)