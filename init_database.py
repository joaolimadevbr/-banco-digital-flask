#!/usr/bin/env/python3
"""
Script para inicializar o banco de dados SQLite
Execute: python init_database.py
"""

import sqlite3
import os

def init_database():
    """Inicializa o banco de dados SQLite"""
    database_file = 'banco.db'
    
    print(f"🗄️ Inicializando banco de dados: {database_file}")
    
    try:
        # Conecta ao banco (cria se não existir)
        db = sqlite3.connect(database_file)
        db.row_factory = sqlite3.Row
        
        print("✅ Conexão com banco estabelecida")
        
        # Cria as tabelas
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
        
        print("✅ Tabelas criadas com sucesso")
        
        # Verifica se as tabelas foram criadas
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 Tabelas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table['name']}")
        
        # Verifica permissões do arquivo
        if os.path.exists(database_file):
            stat = os.stat(database_file)
            print(f"📁 Permissões do arquivo: {oct(stat.st_mode)[-3:]}")
            print(f"📁 Tamanho do arquivo: {stat.st_size} bytes")
        
        db.close()
        print("✅ Banco de dados inicializado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

def test_database():
    """Testa operações básicas no banco"""
    print("\n🧪 Testando operações no banco...")
    
    try:
        db = sqlite3.connect('banco.db')
        db.row_factory = sqlite3.Row
        
        # Testa inserção
        db.execute('INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)',
                  ('Teste', 'teste@teste.com', 'senha_hash'))
        db.commit()
        print("✅ Inserção funcionou")
        
        # Testa consulta
        cursor = db.execute('SELECT * FROM usuario WHERE email = ?', ('teste@teste.com',))
        usuario = cursor.fetchone()
        if usuario:
            print(f"✅ Consulta funcionou - Nome: {usuario['nome']}")
        
        # Limpa dados de teste
        db.execute('DELETE FROM usuario WHERE email = ?', ('teste@teste.com',))
        db.commit()
        print("✅ Deleção funcionou")
        
        db.close()
        print("🎉 Todos os testes passaram!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Iniciando configuração do banco de dados...\n")
    
    # Inicializa o banco
    init_ok = init_database()
    
    if init_ok:
        # Testa operações
        test_ok = test_database()
        
        if test_ok:
            print("\n🎉 Banco de dados configurado e testado com sucesso!")
            print("📋 Próximos passos:")
            print("   1. Execute: python app.py")
            print("   2. Ou para produção: gunicorn app:app")
        else:
            print("\n❌ Testes falharam!")
            exit(1)
    else:
        print("\n❌ Falha na inicialização do banco!")
        exit(1) 