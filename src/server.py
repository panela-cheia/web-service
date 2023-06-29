from flask import Flask
from config import UPLOAD_FOLDER
from routes import routes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(port=3333)
