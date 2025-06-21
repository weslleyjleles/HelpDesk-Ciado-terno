import sqlite3
import os

CAMINHO_BANCO = "helpdesk.db"

def testar_banco():
    if not os.path.exists(CAMINHO_BANCO):
        print("❌ Banco de dados não encontrado!")
        return

    try:
        conn = sqlite3.connect(CAMINHO_BANCO)
        cursor = conn.cursor()

        print("✅ Conexão com o banco de dados estabelecida com sucesso.")

        # Verificar se a tabela chamados existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chamados'")
        resultado = cursor.fetchone()
        if resultado:
            print("✅ Tabela 'chamados' encontrada.")
        else:
            print("❌ Tabela 'chamados' NÃO encontrada.")

        # Teste de inserção e leitura de dados
        print("\n🔍 Chamados existentes (limitado a 5):")
        cursor.execute("SELECT id, titulo, status, usuario, data FROM chamados LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Título: {row[1]} | Status: {row[2]} | Usuário: {row[3]} | Data: {row[4]}")
        
        if not rows:
            print("ℹ️ Nenhum chamado encontrado.")

        conn.close()
    except Exception as e:
        print("❌ Erro ao acessar o banco:", e)

if __name__ == "__main__":
    testar_banco()
