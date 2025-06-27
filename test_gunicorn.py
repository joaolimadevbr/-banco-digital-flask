#!/usr/bin/env python3
"""
Script para testar o Gunicorn localmente
Execute: python test_gunicorn.py
"""

import subprocess
import sys
import os

def test_gunicorn():
    """Testa se o Gunicorn está funcionando corretamente"""
    print("🚀 Testando configuração do Gunicorn...")
    
    try:
        # Verifica se o Gunicorn está instalado
        result = subprocess.run([sys.executable, '-m', 'gunicorn', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Gunicorn instalado:", result.stdout.strip())
        else:
            print("❌ Gunicorn não encontrado. Instalando...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'gunicorn'], check=True)
            print("✅ Gunicorn instalado com sucesso!")
        
        # Testa se a aplicação Flask carrega corretamente
        print("\n🔍 Testando importação da aplicação...")
        from app import app
        print("✅ Aplicação Flask carregada com sucesso!")
        
        # Testa se o banco de dados pode ser criado
        print("\n🗄️ Testando banco de dados...")
        with app.app_context():
            from app import db
            db.create_all()
            print("✅ Banco de dados criado com sucesso!")
        
        print("\n🎉 Todos os testes passaram! A aplicação está pronta para deploy.")
        print("\n📋 Para testar localmente com Gunicorn:")
        print("   gunicorn app:app --bind 0.0.0.0:8000")
        print("\n🌐 Para deploy no Render:")
        print("   1. Faça push para o GitHub")
        print("   2. Conecte no Render.com")
        print("   3. Use: gunicorn app:app como comando de start")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_gunicorn() 