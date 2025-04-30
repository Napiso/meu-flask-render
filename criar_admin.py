from app import create_app
from models import db
from models.user import Usuario

app = create_app()
with app.app_context():
    if not Usuario.query.filter_by(usuario="admin").first():
        user = Usuario(usuario="admin")
        user.set_senha("admin123")
        db.session.add(user)
        db.session.commit()
        print("Usuário admin criado com sucesso.")
    else:
        print("Usuário admin já existe.")
