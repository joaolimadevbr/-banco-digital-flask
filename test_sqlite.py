#!/usr/bin/env python3
"""
Script para testar se o SQLite está funcionando corretamente
Execute: python test_sqlite.py
"""

import sqlite3
import os

def test_sqlite():
    """Testa se o SQLite está funcionando corretamente"""
    print("🔍 Testando SQLite...")
    
    try:
        # Testa conexão
        db = sqlite3.connect(':memory:')
        db.row_factory = sqlite3.Row
        print("✅ Conexão SQLite criada com sucesso!")
        
        # Testa criação de tabelas
        db.executescript('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS conta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                saldo REAL DEFAULT 0.0,
                usuario_id INTEGER NOT NULL
            );
        ''')
        print("✅ Tabelas criadas com sucesso!")
        
        # Testa inserção
        db.execute('INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)',
                  ('Teste', 'teste@teste.com', 'senha_hash'))
        db.commit()
        print("✅ Inserção funcionou!")
        
        # Testa consulta
        cursor = db.execute('SELECT * FROM usuario WHERE email = ?', ('teste@teste.com',))
        usuario = cursor.fetchone()
        if usuario:
            print("✅ Consulta funcionou!")
            print(f"   Nome: {usuario['nome']}")
            print(f"   Email: {usuario['email']}")
        else:
            print("❌ Consulta falhou!")
        
        # Testa atualização
        db.execute('UPDATE usuario SET nome = ? WHERE email = ?', ('Teste Atualizado', 'teste@teste.com'))
        db.commit()
        print("✅ Atualização funcionou!")
        
        # Testa deleção
        db.execute('DELETE FROM usuario WHERE email = ?', ('teste@teste.com',))
        db.commit()
        print("✅ Deleção funcionou!")
        
        db.close()
        print("\n🎉 Todos os testes do SQLite passaram!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no SQLite: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

def test_app_functions():
    """Testa as funções da aplicação"""
    print("\n🔍 Testando funções da aplicação...")
    
    try:
        from app import get_db, init_db
        
        # Testa inicialização do banco
        init_db()
        print("✅ Banco inicializado com sucesso!")
        
        # Testa conexão
        with get_db() as db:
            cursor = db.execute('SELECT name FROM sqlite_master WHERE type="table"')
            tables = cursor.fetchall()
            print(f"✅ Tabelas encontradas: {len(tables)}")
            for table in tables:
                print(f"   - {table['name']}")
        
        print("🎉 Funções da aplicação funcionam corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas funções da aplicação: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do SQLite...\n")
    
    sqlite_ok = test_sqlite()
    app_ok = test_app_functions()
    
    if sqlite_ok and app_ok:
        print("\n🎉 Todos os testes passaram! SQLite está funcionando perfeitamente.")
        print("\n📋 Próximos passos:")
        print("   1. Execute: python app.py")
        print("   2. Ou para produção: gunicorn app:app")
        print("   3. Para deploy no Render, faça push para o GitHub")
    else:
        print("\n❌ Alguns testes falharam.")
        import sys
        sys.exit(1) 