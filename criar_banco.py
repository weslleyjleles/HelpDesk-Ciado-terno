import sqlite3
import os

CAMINHO_BANCO = "helpdesk.db"

def inicializar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    # Criar tabela chamados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            imagem_path TEXT,
            data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Aberto',
            usuario TEXT NOT NULL,
            resposta TEXT
        )
    ''')

    # Criar tabela usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('admin', 'cliente'))
        )
    ''')

    # Verificar se já existe um admin
    cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE tipo = 'admin'")
    existe_admin = cursor.fetchone()[0]

    if not existe_admin:
        # Inserir admin padrão
        cursor.execute('''
            INSERT INTO Usuarios (nome, login, senha, tipo)
            VALUES (?, ?, ?, ?)
        ''', ('Administrador', 'admin', '1234', 'admin'))
        print("✅ Usuário administrador criado: login='admin', senha='1234'")

    conexao.commit()
    conexao.close()
    print("✅ Estrutura do banco verificada/criada com sucesso.")

if __name__ == "__main__":
    inicializar_banco()
