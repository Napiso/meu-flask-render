from datetime import datetime
from . import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    observacao = db.Column(db.String(255))

class Historico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(10))  # 'entrada' ou 'saida'
    pessoa = db.Column(db.String(100))
    obra = db.Column(db.String(100))
    quantidade = db.Column(db.Integer)
    observacao = db.Column(db.String(255))
    data = db.Column(db.DateTime, default=datetime.utcnow)
