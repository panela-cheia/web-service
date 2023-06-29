import os
import random
import string

from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

post_routes = Blueprint('post_routes', __name__)

def generate_random_filename(filename):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    _, ext = os.path.splitext(filename)
    random_filename = f'{random_string}{ext}'
    return f'{filename}-{random_filename}'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in post_routes.config['ALLOWED_EXTENSIONS']

@post_routes.route('/posts', methods=['GET'])
def get_posts():
    # Implement your logic to retrieve posts from the database
    posts = []

    return jsonify(posts)

@post_routes.route('/posts', methods=['POST'])
def create_post():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = generate_random_filename(filename)
        file_path = os.path.join(post_routes.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Implement your logic to create a post in the database
        post = {
            'name': filename,
            'size': os.path.getsize(file_path),
            'url': f'/files/{filename}'
        }

        return jsonify(post), 201

    return jsonify({'error': 'Invalid file type'}), 400

@post_routes.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    # Implement your logic to delete the post from the database

    return '', 204

@post_routes.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(post_routes.config['UPLOAD_FOLDER'], filename)