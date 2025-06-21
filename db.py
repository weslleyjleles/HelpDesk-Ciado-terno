import sqlite3
import os

CAMINHO_BANCO = "helpdesk.db"

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def inicializar_banco():
    if not os.path.exists(CAMINHO_BANCO):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                imagem_path TEXT,
                data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Aberto',
                usuario TEXT,
                resposta TEXT
            )
        """)
        conn.commit()
        conn.close()
import sqlite3
import os

CAMINHO_BANCO = "helpdesk.db"

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def inicializar_banco():
    if not os.path.exists(CAMINHO_BANCO):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                descricao TEXT,
                anexo TEXT,
                data TEXT,
                status TEXT DEFAULT 'Aberto',
                usuario TEXT,
                resposta TEXT
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Banco e tabela 'chamados' criados com sucesso.")
    else:
        print("ℹ️ Banco já existe.")
