from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models.models import db
from models.user import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and user.check_senha(senha):
            session['usuario'] = usuario
            return redirect(url_for('main.index'))
        flash('Usuário ou senha incorretos.')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('auth.login'))
