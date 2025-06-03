from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import *

@app.route("/")
def home():
    return "Projeto Flask está rodando com PostgreSQL!"

if __name__ == "__main__":
    app.run()