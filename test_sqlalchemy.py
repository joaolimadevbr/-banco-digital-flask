#!/usr/bin/env python3
"""
Script para testar se o SQLAlchemy está funcionando corretamente
Execute: python test_sqlalchemy.py
"""

import os
import sys

def test_sqlalchemy():
    """Testa se o SQLAlchemy está funcionando corretamente"""
    print("🔍 Testando SQLAlchemy...")
    
    try:
        # Testa importação
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask e Flask-SQLAlchemy importados com sucesso!")
        
        # Cria app de teste
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        print("✅ SQLAlchemy inicializado com sucesso!")
        
        # Testa modelo simples
        class TestModel(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(100))
        
        with app.app_context():
            # Cria tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Testa operações básicas
            test_item = TestModel(name="Teste")
            db.session.add(test_item)
            db.session.commit()
            print("✅ Inserção no banco funcionou!")
            
            # Testa consulta
            result = db.session.query(TestModel).filter_by(name="Teste").first()
            if result:
                print("✅ Consulta no banco funcionou!")
            else:
                print("❌ Consulta falhou!")
            
            # Limpa
            db.session.delete(test_item)
            db.session.commit()
            print("✅ Deleção funcionou!")
        
        print("\n🎉 Todos os testes do SQLAlchemy passaram!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no SQLAlchemy: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

def test_app_models():
    """Testa os modelos da aplicação"""
    print("\n🔍 Testando modelos da aplicação...")
    
    try:
        from app import app, db, Usuario, Conta, Transacao
        
        with app.app_context():
            # Cria tabelas
            db.create_all()
            print("✅ Modelos da aplicação criados com sucesso!")
            
            # Testa criação de usuário
            from werkzeug.security import generate_password_hash
            usuario = Usuario(
                nome="Teste",
                email="teste@teste.com",
                senha=generate_password_hash("123456")
            )
            db.session.add(usuario)
            db.session.commit()
            print("✅ Usuário criado com sucesso!")
            
            # Testa criação de conta
            conta = Conta(
                tipo="corrente",
                usuario_id=usuario.id
            )
            db.session.add(conta)
            db.session.commit()
            print("✅ Conta criada com sucesso!")
            
            # Testa criação de transação
            transacao = Transacao(
                tipo="deposito",
                valor=100.0,
                descricao="Teste",
                conta_id=conta.id
            )
            db.session.add(transacao)
            db.session.commit()
            print("✅ Transação criada com sucesso!")
            
            # Limpa dados de teste
            db.session.delete(transacao)
            db.session.delete(conta)
            db.session.delete(usuario)
            db.session.commit()
            print("✅ Dados de teste removidos!")
        
        print("🎉 Todos os modelos da aplicação funcionam corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos modelos da aplicação: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do SQLAlchemy...\n")
    
    sqlalchemy_ok = test_sqlalchemy()
    models_ok = test_app_models()
    
    if sqlalchemy_ok and models_ok:
        print("\n🎉 Todos os testes passaram! SQLAlchemy está funcionando perfeitamente.")
        print("\n📋 Próximos passos:")
        print("   1. Execute: python app.py")
        print("   2. Ou para produção: gunicorn app:app")
        print("   3. Para deploy no Render, faça push para o GitHub")
    else:
        print("\n❌ Alguns testes falharam. Verifique as dependências:")
        print("   pip install -r requirements.txt")
        sys.exit(1) 