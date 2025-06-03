from flask import Flask
from models import db
from routes.main import main
from routes.auth import auth
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=80)
