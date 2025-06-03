from flask import Flask
from config import Config
from models import db
from routes.main import main
from routes.auth import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
