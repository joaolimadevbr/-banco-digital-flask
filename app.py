from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')

# Configuração do banco SQLite
DATABASE = 'banco.db'

def get_db():
    """Conecta ao banco de dados SQLite"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Inicializa o banco de dados com as tabelas"""
    try:
        with get_db() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    saldo REAL DEFAULT 0.0,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS conta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    saldo REAL DEFAULT 0.0,
                    usuario_id INTEGER NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
                );
                
                CREATE TABLE IF NOT EXISTS transacao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    valor REAL NOT NULL,
                    descricao TEXT,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    conta_id INTEGER NOT NULL,
                    FOREIGN KEY (conta_id) REFERENCES conta (id)
                );
            ''')
            print("✅ Banco de dados SQLite inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")

# Inicializa o banco quando o app é criado
init_db()

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
        
        try:
            with get_db() as db:
                # Verifica se email já existe
                cursor = db.execute('SELECT id FROM usuario WHERE email = ?', (email,))
                if cursor.fetchone():
                    flash('Email já cadastrado!', 'error')
                    return redirect(url_for('registro'))
                
                # Cria novo usuário
                senha_hash = generate_password_hash(senha)
                db.execute('INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)',
                          (nome, email, senha_hash))
                db.commit()
            
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('login'))
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                # Se a tabela não existe, tenta criar novamente
                init_db()
                flash('Erro temporário. Tente novamente.', 'error')
                return redirect(url_for('registro'))
            else:
                flash('Erro no banco de dados!', 'error')
                return redirect(url_for('registro'))
        except Exception as e:
            flash('Erro inesperado!', 'error')
            return redirect(url_for('registro'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            with get_db() as db:
                cursor = db.execute('SELECT * FROM usuario WHERE email = ?', (email,))
                usuario = cursor.fetchone()
                
                if usuario and check_password_hash(usuario['senha'], senha):
                    session['usuario_id'] = usuario['id']
                    session['usuario_nome'] = usuario['nome']
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Email ou senha incorretos!', 'error')
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                init_db()
                flash('Erro temporário. Tente novamente.', 'error')
            else:
                flash('Erro no banco de dados!', 'error')
        except Exception as e:
            flash('Erro inesperado!', 'error')
    
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
    
    try:
        with get_db() as db:
            # Busca usuário
            cursor = db.execute('SELECT * FROM usuario WHERE id = ?', (session['usuario_id'],))
            usuario = cursor.fetchone()
            
            if not usuario:
                session.clear()
                flash('Usuário não encontrado!', 'error')
                return redirect(url_for('login'))
            
            # Busca contas do usuário
            cursor = db.execute('SELECT * FROM conta WHERE usuario_id = ?', (usuario['id'],))
            contas = cursor.fetchall()
        
        return render_template('dashboard.html', usuario=usuario, contas=contas)
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            init_db()
            flash('Erro temporário. Recarregue a página.', 'error')
            return redirect(url_for('login'))
        else:
            flash('Erro no banco de dados!', 'error')
            return redirect(url_for('login'))
    except Exception as e:
        flash('Erro inesperado!', 'error')
        return redirect(url_for('login'))

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        usuario_id = session['usuario_id']
        
        try:
            with get_db() as db:
                db.execute('INSERT INTO conta (tipo, usuario_id) VALUES (?, ?)',
                          (tipo, usuario_id))
                db.commit()
            
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                init_db()
                flash('Erro temporário. Tente novamente.', 'error')
            else:
                flash('Erro no banco de dados!', 'error')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Erro inesperado!', 'error')
            return redirect(url_for('dashboard'))
    
    return render_template('criar_conta.html')

@app.route('/deposito/<int:conta_id>', methods=['GET', 'POST'])
def deposito(conta_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with get_db() as db:
            # Verifica se a conta pertence ao usuário
            cursor = db.execute('SELECT * FROM conta WHERE id = ? AND usuario_id = ?',
                              (conta_id, session['usuario_id']))
            conta = cursor.fetchone()
            
            if not conta:
                flash('Acesso negado!', 'error')
                return redirect(url_for('dashboard'))
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            init_db()
            flash('Erro temporário. Tente novamente.', 'error')
        else:
            flash('Erro no banco de dados!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            valor = float(request.form['valor'])
            if valor > 0:
                with get_db() as db:
                    # Atualiza saldo
                    db.execute('UPDATE conta SET saldo = saldo + ? WHERE id = ?',
                              (valor, conta_id))
                    
                    # Registra transação
                    db.execute('INSERT INTO transacao (tipo, valor, descricao, conta_id) VALUES (?, ?, ?, ?)',
                              ('deposito', valor, 'Depósito', conta_id))
                    db.commit()
                
                flash('Depósito realizado com sucesso!', 'success')
            else:
                flash('Valor deve ser maior que zero!', 'error')
        except ValueError:
            flash('Valor inválido!', 'error')
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                init_db()
                flash('Erro temporário. Tente novamente.', 'error')
            else:
                flash('Erro no banco de dados!', 'error')
        except Exception as e:
            flash('Erro inesperado!', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('deposito.html', conta=conta)

@app.route('/saque/<int:conta_id>', methods=['GET', 'POST'])
def saque(conta_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with get_db() as db:
            # Verifica se a conta pertence ao usuário
            cursor = db.execute('SELECT * FROM conta WHERE id = ? AND usuario_id = ?',
                              (conta_id, session['usuario_id']))
            conta = cursor.fetchone()
            
            if not conta:
                flash('Acesso negado!', 'error')
                return redirect(url_for('dashboard'))
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            init_db()
            flash('Erro temporário. Tente novamente.', 'error')
        else:
            flash('Erro no banco de dados!', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            valor = float(request.form['valor'])
            if valor > 0 and valor <= conta['saldo']:
                with get_db() as db:
                    # Atualiza saldo
                    db.execute('UPDATE conta SET saldo = saldo - ? WHERE id = ?',
                              (valor, conta_id))
                    
                    # Registra transação
                    db.execute('INSERT INTO transacao (tipo, valor, descricao, conta_id) VALUES (?, ?, ?, ?)',
                              ('saque', valor, 'Saque', conta_id))
                    db.commit()
                
                flash('Saque realizado com sucesso!', 'success')
            else:
                flash('Valor inválido ou saldo insuficiente!', 'error')
        except ValueError:
            flash('Valor inválido!', 'error')
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                init_db()
                flash('Erro temporário. Tente novamente.', 'error')
            else:
                flash('Erro no banco de dados!', 'error')
        except Exception as e:
            flash('Erro inesperado!', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('saque.html', conta=conta)

@app.route('/extrato/<int:conta_id>')
def extrato(conta_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with get_db() as db:
            # Verifica se a conta pertence ao usuário
            cursor = db.execute('SELECT * FROM conta WHERE id = ? AND usuario_id = ?',
                              (conta_id, session['usuario_id']))
            conta = cursor.fetchone()
            
            if not conta:
                flash('Acesso negado!', 'error')
                return redirect(url_for('dashboard'))
            
            # Busca transações
            cursor = db.execute('SELECT * FROM transacao WHERE conta_id = ? ORDER BY data DESC',
                              (conta_id,))
            transacoes = cursor.fetchall()
        
        return render_template('extrato.html', conta=conta, transacoes=transacoes)
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            init_db()
            flash('Erro temporário. Tente novamente.', 'error')
        else:
            flash('Erro no banco de dados!', 'error')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash('Erro inesperado!', 'error')
        return redirect(url_for('dashboard'))

# Rota de health check para o Render
@app.route('/health')
def health_check():
    try:
        # Testa conexão com banco
        with get_db() as db:
            cursor = db.execute('SELECT COUNT(*) as count FROM usuario')
            user_count = cursor.fetchone()['count']
        
        return {
            'status': 'healthy', 
            'message': 'Banco Digital API está funcionando!',
            'database': 'connected',
            'users_count': user_count
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Erro no banco de dados: {str(e)}',
            'database': 'disconnected'
        }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 