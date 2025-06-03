from flask import Flask
from models import db
from routes.main import main
from config import Config
from routes.auth import auth

def create_app():
    app = Flask(__name__)
    app.secret_key = 'minha-chave-super-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.config.from_object(Config)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=80)
