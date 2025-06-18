import os
import json
from PIL import Image
import customtkinter

CAMINHO_IMAGENS = "imagens"
CAMINHO_CHAMADOS = "chamados.json"
IMAGEM_PADRAO = "padrao.png"  # Nome de uma imagem padrão que deve existir na pasta "imagens"

def carregar_imagem(nome_arquivo, tamanho):
    caminho = os.path.join(CAMINHO_IMAGENS, nome_arquivo)
    if os.path.exists(caminho):
        return customtkinter.CTkImage(light_image=Image.open(caminho), size=tamanho)
    else:
        caminho_padrao = os.path.join(CAMINHO_IMAGENS, IMAGEM_PADRAO)
        if os.path.exists(caminho_padrao):
            print(f"[AVISO] Imagem {nome_arquivo} não encontrada. Usando imagem padrão.")
            return customtkinter.CTkImage(light_image=Image.open(caminho_padrao), size=tamanho)
        else:
            print(f"[ERRO] Imagem {nome_arquivo} e imagem padrão não encontradas.")
            return None

def carregar_chamados():
    try:
        with open(CAMINHO_CHAMADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("chamados", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_chamados(lista_chamados):
    with open(CAMINHO_CHAMADOS, "w", encoding="utf-8") as f:
        json.dump({"chamados": lista_chamados}, f, indent=4, ensure_ascii=False)
