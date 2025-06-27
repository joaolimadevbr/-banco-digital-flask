from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração para PostgreSQL no Render
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)

# Modelos do banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    saldo = db.Column(db.Float, default=0.0)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    contas = db.relationship('Conta', backref='usuario', lazy=True)

class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # 'corrente', 'poupanca'
    saldo = db.Column(db.Float, default=0.0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    transacoes = db.relationship('Transacao', backref='conta', lazy=True)

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # 'deposito', 'saque', 'transferencia'
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False)

# Rotas
@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return redirect(url_for('registro'))
        
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    contas = Conta.query.filter_by(usuario_id=usuario.id).all()
    return render_template('dashboard.html', usuario=usuario, contas=contas)

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        usuario_id = session['usuario_id']
        
        nova_conta = Conta(tipo=tipo, usuario_id=usuario_id)
        db.session.add(nova_conta)
        db.session.commit()
        
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('criar_conta.html')

@app.route('/deposito/<int:conta_id>', methods=['GET', 'POST'])
def deposito(conta_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    conta = Conta.query.get_or_404(conta_id)
    if conta.usuario_id != session['usuario_id']:
        flash('Acesso negado!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        valor = float(request.form['valor'])
        if valor > 0:
            conta.saldo += valor
            transacao = Transacao(tipo='deposito', valor=valor, 
                                 descricao='Depósito', conta_id=conta.id)
            db.session.add(transacao)
            db.session.commit()
            flash('Depósito realizado com sucesso!', 'success')
        else:
            flash('Valor deve ser maior que zero!', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('deposito.html', conta=conta)

@app.route('/saque/<int:conta_id>', methods=['GET', 'POST'])
def saque(conta_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    conta = Conta.query.get_or_404(conta_id)
    if conta.usuario_id != session['usuario_id']:
        flash('Acesso negado!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        valor = float(request.form['valor'])
        if valor > 0 and valor <= conta.saldo:
            conta.saldo -= valor
            transacao = Transacao(tipo='saque', valor=valor, 
                                 descricao='Saque', conta_id=conta.id)
            db.session.add(transacao)
            db.session.commit()
            flash('Saque realizado com sucesso!', 'success')
        else:
            flash('Valor inválido ou saldo insuficiente!', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('saque.html', conta=conta)

@app.route('/extrato/<int:conta_id>')
def extrato(conta_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    conta = Conta.query.get_or_404(conta_id)
    if conta.usuario_id != session['usuario_id']:
        flash('Acesso negado!', 'error')
        return redirect(url_for('dashboard'))
    
    transacoes = Transacao.query.filter_by(conta_id=conta.id).order_by(Transacao.data.desc()).all()
    return render_template('extrato.html', conta=conta, transacoes=transacoes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 