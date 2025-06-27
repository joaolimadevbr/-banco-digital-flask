# 🗄️ Migração para SQLite

Este documento explica a migração do projeto de SQLAlchemy para SQLite direto.

## 🔄 Mudanças Realizadas

### ❌ **Removido:**
- SQLAlchemy e Flask-SQLAlchemy
- Modelos ORM (Usuario, Conta, Transacao)
- Configurações complexas de banco

### ✅ **Adicionado:**
- SQLite nativo do Python
- Queries SQL diretas
- Funções de conexão simplificadas

## 📊 Comparação

### **Antes (SQLAlchemy):**
```python
# Modelo ORM
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    # ...

# Consulta
usuario = Usuario.query.filter_by(email=email).first()
```

### **Depois (SQLite):**
```python
# Tabela SQL
CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    # ...
);

# Consulta
cursor = db.execute('SELECT * FROM usuario WHERE email = ?', (email,))
usuario = cursor.fetchone()
```

## 🛠️ Vantagens do SQLite

### ✅ **Simplicidade:**
- Sem dependências externas
- Código mais direto e legível
- Menos problemas de compatibilidade

### ✅ **Performance:**
- Mais rápido para aplicações pequenas
- Menos overhead
- Banco de dados em arquivo único

### ✅ **Deploy:**
- Funciona em qualquer ambiente
- Sem configuração de servidor de banco
- Ideal para Render e outros PaaS

## 📁 Estrutura do Banco

### **Tabelas Criadas:**
```sql
-- Usuários
CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    saldo REAL DEFAULT 0.0,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contas
CREATE TABLE conta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    saldo REAL DEFAULT 0.0,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);

-- Transações
CREATE TABLE transacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    valor REAL NOT NULL,
    descricao TEXT,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    conta_id INTEGER NOT NULL,
    FOREIGN KEY (conta_id) REFERENCES conta (id)
);
```

## 🔧 Funções Principais

### **Conexão:**
```python
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db
```

### **Inicialização:**
```python
def init_db():
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS usuario (...);
            CREATE TABLE IF NOT EXISTS conta (...);
            CREATE TABLE IF NOT EXISTS transacao (...);
        ''')
```

## 📦 Dependências Atualizadas

### **requirements.txt:**
```
Flask==2.3.3
Werkzeug==2.3.7
gunicorn==21.2.0
```

**Removido:**
- Flask-SQLAlchemy==3.0.5
- SQLAlchemy==2.0.23

## 🧪 Testes

### **test_sqlite.py:**
- Testa conexão SQLite
- Testa operações CRUD
- Testa funções da aplicação

### **Resultado:**
```
✅ Conexão SQLite criada com sucesso!
✅ Tabelas criadas com sucesso!
✅ Inserção funcionou!
✅ Consulta funcionou!
✅ Atualização funcionou!
✅ Deleção funcionou!
```

## 🚀 Deploy

### **Render.yaml (Simplificado):**
```yaml
services:
  - type: web
    name: banco-digital-flask
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
      - key: SECRET_KEY
        generateValue: true
```

### **Vantagens:**
- Sem configuração de banco externo
- Deploy mais simples
- Menos pontos de falha

## 📋 Checklist de Migração

- [x] Removido SQLAlchemy
- [x] Implementado SQLite nativo
- [x] Criadas tabelas SQL
- [x] Atualizadas todas as rotas
- [x] Testes funcionando
- [x] Dependências atualizadas
- [x] Deploy configurado

## 🎯 Resultado

✅ **Aplicação mais simples e robusta**
✅ **Menos dependências**
✅ **Deploy mais fácil**
✅ **Performance melhorada**
✅ **Código mais legível**

---

**Status:** ✅ **Migração concluída com sucesso!** 