#!/usr/bin/env python3
"""
Script para testar a funcionalidade do extrato
Execute: python test_extrato.py
"""

import sqlite3
from datetime import datetime

def test_extrato():
    """Testa a funcionalidade do extrato"""
    print("🔍 Testando funcionalidade do extrato...")
    
    try:
        # Conecta ao banco
        db = sqlite3.connect('banco.db')
        db.row_factory = sqlite3.Row
        
        # Cria dados de teste
        print("📝 Criando dados de teste...")
        
        # Cria usuário de teste
        db.execute('INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)',
                  ('Teste Extrato', 'teste@extrato.com', 'senha_hash'))
        db.commit()
        
        # Busca ID do usuário
        cursor = db.execute('SELECT id FROM usuario WHERE email = ?', ('teste@extrato.com',))
        usuario = cursor.fetchone()
        usuario_id = usuario['id']
        
        # Cria conta de teste
        db.execute('INSERT INTO conta (tipo, usuario_id) VALUES (?, ?)',
                  ('corrente', usuario_id))
        db.commit()
        
        # Busca ID da conta
        cursor = db.execute('SELECT id FROM conta WHERE usuario_id = ?', (usuario_id,))
        conta = cursor.fetchone()
        conta_id = conta['id']
        
        # Cria transações de teste
        transacoes_teste = [
            ('deposito', 100.0, 'Depósito inicial'),
            ('saque', 30.0, 'Saque teste'),
            ('deposito', 50.0, 'Depósito adicional')
        ]
        
        for tipo, valor, descricao in transacoes_teste:
            db.execute('INSERT INTO transacao (tipo, valor, descricao, conta_id) VALUES (?, ?, ?, ?)',
                      (tipo, valor, descricao, conta_id))
        db.commit()
        
        print("✅ Dados de teste criados")
        
        # Testa consulta do extrato
        print("🔍 Testando consulta do extrato...")
        
        cursor = db.execute('''
            SELECT 
                id, tipo, valor, descricao, conta_id,
                strftime('%d/%m/%Y %H:%M', data) as data_formatada
            FROM transacao 
            WHERE conta_id = ? 
            ORDER BY data DESC
        ''', (conta_id,))
        
        transacoes = cursor.fetchall()
        
        print(f"✅ Encontradas {len(transacoes)} transações")
        
        # Mostra as transações
        for i, transacao in enumerate(transacoes, 1):
            print(f"   {i}. {transacao['data_formatada']} - {transacao['tipo'].title()} - R$ {transacao['valor']:.2f}")
        
        # Testa formatação de data
        print("\n📅 Testando formatação de data...")
        cursor = db.execute('SELECT data, strftime("%d/%m/%Y %H:%M", data) as formatada FROM transacao LIMIT 1')
        resultado = cursor.fetchone()
        print(f"   Data original: {resultado['data']}")
        print(f"   Data formatada: {resultado['formatada']}")
        
        # Limpa dados de teste
        print("\n🧹 Limpando dados de teste...")
        db.execute('DELETE FROM transacao WHERE conta_id = ?', (conta_id,))
        db.execute('DELETE FROM conta WHERE id = ?', (conta_id,))
        db.execute('DELETE FROM usuario WHERE id = ?', (usuario_id,))
        db.commit()
        
        db.close()
        print("✅ Teste do extrato concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do extrato: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

if __name__ == '__main__':
    print("🚀 Iniciando teste do extrato...\n")
    
    if test_extrato():
        print("\n🎉 Teste do extrato passou!")
        print("📋 O extrato deve funcionar corretamente agora.")
    else:
        print("\n❌ Teste do extrato falhou!")
        import sys
        sys.exit(1) 