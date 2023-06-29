import os
import random
import string
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import boto3

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png', 'gif'])

load_dotenv()

def generate_random_filename(filename):
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))
    _, ext = os.path.splitext(filename)
    random_filename = f'{random_string}{ext}'
    return f'{filename}-{random_filename}'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def upload_local(file, filename):
    upload_folder = 'tmp/uploads'
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def upload_s3(file, filename):
    s3_bucket = os.getenv('S3_BUCKET_NAME')
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(file, s3_bucket, filename)
    file_url = f'https://{s3_bucket}.s3.amazonaws.com/{filename}'
    return file_url

def create_post():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    upload_option = os.getenv('UPLOAD_CONFIG_DEVELOPMENT')

    if upload_option == 'local':
        file_path = upload_local(file, filename)
        file_url = f'/files/{filename}'
    elif upload_option == 's3':
        file_url = upload_s3(file, filename)
    else:
        return jsonify({'error': 'Invalid upload option'}), 400

    # Implement your logic to create a post in the database
    post = {
        'name': filename,
        'size': os.path.getsize(file_path),
        'url': file_url
    }

    return jsonify(post), 201

# Resto do código...

if __name__ == '__main__':
    app.run(port=3333, debug=True)