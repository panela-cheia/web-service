import os

from flask import Flask

def upload_local(app:Flask,file, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    base_url = os.getenv('BASE_URL')
    file_url = f'{base_url}/files/{filename}'
    return file_url