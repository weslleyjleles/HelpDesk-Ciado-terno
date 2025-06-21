import os
from PIL import Image
import customtkinter
from db import conectar, inicializar_banco
import sqlite3


# Inicializa o banco SQLite
inicializar_banco()

# Caminhos
CAMINHO_IMAGENS = "imagens"
IMAGEM_PADRAO = "padrao.png"

def carregar_imagem(nome_arquivo, tamanho):
    caminho = os.path.join(CAMINHO_IMAGENS, nome_arquivo)
    if os.path.exists(caminho):
        return customtkinter.CTkImage(light_image=Image.open(caminho), size=tamanho)
    else:
        caminho_padrao = os.path.join(CAMINHO_IMAGENS, IMAGEM_PADRAO)
        if os.path.exists(caminho_padrao):
            print(f"[AVISO] Imagem '{nome_arquivo}' não encontrada. Usando imagem padrão.")
            return customtkinter.CTkImage(light_image=Image.open(caminho_padrao), size=tamanho)
        else:
            print(f"[ERRO] Imagem '{nome_arquivo}' e imagem padrão não encontradas.")
            return None

def salvar_chamado_sql(titulo, descricao, imagem_path, usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Chamados (titulo, descricao, imagem_path, status, usuario)
            VALUES (?, ?, ?, 'Aberto', ?)
        """, (titulo, descricao, imagem_path, usuario))
        conn.commit()
    except Exception as e:
        print(f"[ERRO] Erro ao salvar chamado: {e}")
        raise
    finally:
        conn.close()

def salvar_resposta_chamado(chamado_id, resposta):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Chamados
            SET resposta = ?
            WHERE id = ?
        """, (resposta, chamado_id))
        conn.commit()
    except Exception as e:
        print(f"[ERRO] Erro ao salvar resposta: {e}")
        raise
    finally:
        conn.close()

def atualizar_status_chamado(chamado_id, novo_status):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Chamados
            SET status = ?
            WHERE id = ?
        """, (novo_status, chamado_id))
        conn.commit()
    except Exception as e:
        print(f"[ERRO] Erro ao atualizar status: {e}")
        raise
    finally:
        conn.close()

def carregar_chamados_sql():
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row  # permite acessar por nome
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, titulo, descricao, imagem_path, data_abertura, status, usuario, resposta
            FROM Chamados
        """)
        resultados = cursor.fetchall()
        chamados = []
        for row in resultados:
            chamados.append({
                "id": row["id"],
                "titulo": row["titulo"],
                "descricao": row["descricao"],
                "anexo": row["imagem_path"],
                "data": row["data_abertura"],
                "status": row["status"],
                "usuario": row["usuario"],
                "setor": "TI",  # campo fixo ou você pode ajustar se desejar
                "resposta": row["resposta"]
            })
        return chamados
    except Exception as e:
        print(f"[ERRO] Erro ao carregar chamados: {e}")
        return []
    finally:
        conn.close()

# Aliases para compatibilidade
carregar_chamados = carregar_chamados_sql
salvar_chamados = salvar_chamado_sql
