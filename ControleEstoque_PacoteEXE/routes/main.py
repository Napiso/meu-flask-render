from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import db, Produto, Historico
from datetime import datetime
from utils.excel import exportar_excel

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    filtro_produto = request.args.get('filtro_produto', '').strip().lower()
    filtro_obra = request.args.get('filtro_obra', '').strip().lower()
    filtro_obra = request.args.get('filtro_obra', '').strip().lower()

    produtos_query = Produto.query
    historico_query = Historico.query.order_by(Historico.data.desc())

    if filtro_produto:
        produtos_query = produtos_query.filter(Produto.nome.ilike(f"%{filtro_produto}%"))
        historico_query = historico_query.filter(Historico.produto_nome.ilike(f"%{filtro_produto}%"))

    if filtro_obra:
        historico_query = historico_query.filter(Historico.obra.ilike(f"%{filtro_obra}%"))

    if filtro_obra:
        produtos_usados = db.session.query(Historico.produto_nome).filter(Historico.obra.ilike(f"%{filtro_obra}%")).distinct().all()
        nomes_usados = [p[0] for p in produtos_usados]
        produtos_query = produtos_query.filter(Produto.nome.in_(nomes_usados))

    produtos = produtos_query.all()
    # Criar dicionário com última obra por produto
    ultimas_obras = {}
    for p in produtos:
        ultima = Historico.query.filter_by(produto_nome=p.nome).order_by(Historico.data.desc()).first()
        ultimas_obras[p.nome] = ultima.obra if ultima else "---"
    
    historico = historico_query.limit(50).all()
    import pytz
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    for h in historico:
        h.data = h.data.astimezone(fuso_brasilia)

    return render_template('index.html', ultimas_obras=ultimas_obras,
    labels=[p.nome for p in produtos],
    values=[p.quantidade for p in produtos],
                           produtos=produtos,
                           historico=historico,
                           filtro_produto=filtro_produto,
                           filtro_obra=filtro_obra)

@main.route('/exportar/estoque')
def exportar_estoque():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    filtro_produto = request.args.get('filtro_produto', '').strip().lower()
    filtro_obra = request.args.get('filtro_obra', '').strip().lower()

    produtos_query = Produto.query
    if filtro_produto:
        produtos_query = produtos_query.filter(Produto.nome.ilike(f"%{filtro_produto}%"))

    if filtro_obra:
        produtos_usados = db.session.query(Historico.produto_nome).filter(
            Historico.obra.ilike(f"%{filtro_obra}%")
        ).distinct().all()
        nomes_usados = [p[0] for p in produtos_usados]
        produtos_query = produtos_query.filter(Produto.nome.in_(nomes_usados))

    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    filtro_produto = request.args.get('filtro_produto', '').strip().lower()
    filtro_obra = request.args.get('filtro_obra', '').strip().lower()
    produtos_query = Produto.query
    if filtro_produto:
        produtos_query = produtos_query.filter(Produto.nome.ilike(f"%{filtro_produto}%"))
    if filtro_obra:
        produtos_usados = db.session.query(Historico.produto_nome).filter(Historico.obra.ilike(f"%{filtro_obra}%")).distinct().all()
        nomes_usados = [p[0] for p in produtos_usados]
        produtos_query = produtos_query.filter(Produto.nome.in_(nomes_usados))

    produtos = produtos_query.all()
    # Criar dicionário com última obra por produto
    ultimas_obras = {}
    for p in produtos:
        ultima = Historico.query.filter_by(produto_nome=p.nome).order_by(Historico.data.desc()).first()
        ultimas_obras[p.nome] = ultima.obra if ultima else "---"
    

    colunas = ['Produto', 'Quantidade', 'Última Obra', 'Observação']
    dados = [(p.nome, p.quantidade, ultimas_obras.get(p.nome, '---'), p.observacao or '') for p in produtos]
    return exportar_excel('Estoque', colunas, dados)

@main.route('/exportar/historico')
def exportar_historico():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    filtro_produto = request.args.get('filtro_produto', '').strip().lower()
    filtro_obra = request.args.get('filtro_obra', '').strip().lower()
    filtro_obra = request.args.get('filtro_obra', '').strip().lower()

    historico_query = Historico.query.order_by(Historico.data.desc())
    if filtro_produto:
        historico_query = historico_query.filter(Historico.produto_nome.ilike(f"%{filtro_produto}%"))
    if filtro_obra:
        historico_query = historico_query.filter(Historico.obra.ilike(f"%{filtro_obra}%"))

    historico = historico_query.all()
    colunas = ['Data', 'Produto', 'Tipo', 'Quantidade', 'Obra', 'Pessoa', 'Observação']
    dados = [(h.data.strftime('%d/%m/%Y %H:%M'), h.produto_nome, h.tipo, h.quantidade, h.obra, h.pessoa, h.observacao or '') for h in historico]
    return exportar_excel('Historico', colunas, dados)

@main.route('/add', methods=['POST'])
def add():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    nome = request.form.get('produto', '').strip().title()
    entrada_str = request.form.get('entrada', '0')
    saida_str = request.form.get('saida', '0')
    pessoa = request.form.get('pessoa', '').strip()
    observacao = request.form.get('observacao', '').strip()
    obra = request.form.get('obra', '').strip()

    entrada = int(entrada_str) if entrada_str.isdigit() else 0
    saida = int(saida_str) if saida_str.isdigit() else 0

    produto = Produto.query.filter_by(nome=nome).first()

    if not produto:
        if entrada == 0:
            erro = "Erro: produto não existe no estoque e nenhuma entrada foi informada."
            produtos = Produto.query.all()
            historico = Historico.query.order_by(Historico.data.desc()).limit(50).all()
            ultimas_obras = {}
            for p in produtos:
                ultima = Historico.query.filter_by(produto_nome=p.nome).order_by(Historico.data.desc()).first()
                ultimas_obras[p.nome] = ultima.obra if ultima else "---"
            return render_template('index.html', produtos=produtos, historico=historico,
                                   ultimas_obras=ultimas_obras,
    labels=[p.nome for p in produtos],
    values=[p.quantidade for p in produtos], erro=erro,
                                   filtro_produto='', filtro_obra='')
        produto = Produto(nome=nome, quantidade=0, observacao=observacao)
        db.session.add(produto)

    if saida > 0:
        if saida > produto.quantidade:
            erro = f"Erro: saída ({saida}) maior que o estoque disponível ({produto.quantidade})."
            produtos = Produto.query.all()
            historico = Historico.query.order_by(Historico.data.desc()).limit(50).all()
            ultimas_obras = {}
            for p in produtos:
                ultima = Historico.query.filter_by(produto_nome=p.nome).order_by(Historico.data.desc()).first()
                ultimas_obras[p.nome] = ultima.obra if ultima else "---"
            return render_template('index.html', produtos=produtos, historico=historico,
                                   ultimas_obras=ultimas_obras,
    labels=[p.nome for p in produtos],
    values=[p.quantidade for p in produtos], erro=erro,
                                   filtro_produto='', filtro_obra='')

        produto.quantidade -= saida
        db.session.add(Historico(produto_nome=nome, tipo='saida', pessoa=pessoa,
                                 quantidade=saida, observacao=observacao, obra=obra))

    if entrada > 0:
        produto.quantidade += entrada
        db.session.add(Historico(produto_nome=nome, tipo='entrada', pessoa=pessoa,
                                 quantidade=entrada, observacao=observacao, obra=obra))

    if observacao:
        produto.observacao = observacao

    db.session.commit()
    return redirect(url_for('main.index'))

    produto = Produto.query.filter_by(nome=nome).first()
    if not produto and entrada == 0:
        erro = "Erro: produto não existe no estoque e nenhuma entrada foi informada."
        produtos = Produto.query.all()
        historico = Historico.query.order_by(Historico.data.desc()).limit(50).all()
        ultimas_obras = {}
        for p in produtos:
            ultima = Historico.query.filter_by(produto_nome=p.nome).order_by(Historico.data.desc()).first()
            ultimas_obras[p.nome] = ultima.obra if ultima else "---"
        return render_template('index.html', produtos=produtos, historico=historico,
                               ultimas_obras=ultimas_obras,
    labels=[p.nome for p in produtos],
    values=[p.quantidade for p in produtos], erro=erro,
                               filtro_produto='', filtro_obra='')
    produto = Produto(nome=nome, quantidade=0, observacao=observacao)
    db.session.add(produto)

    if entrada > 0:
        produto.quantidade += entrada
        historico = Historico(produto_nome=nome, tipo='entrada', pessoa=pessoa,
                              quantidade=entrada, observacao=observacao, obra=obra)
        db.session.add(historico)

    if saida > 0:
        produto.quantidade = max(0, produto.quantidade - saida)
        historico = Historico(produto_nome=nome, tipo='saida', pessoa=pessoa,
                              quantidade=saida, observacao=observacao, obra=obra)
        db.session.add(historico)

    if observacao:
        produto.observacao = observacao

    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete/<int:produto_id>')

@main.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('main.index'))
