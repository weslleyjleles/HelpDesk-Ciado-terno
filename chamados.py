import customtkinter
from tkinter import messagebox, filedialog, ttk
from PIL import Image
import os
import shutil
import csv
from datetime import datetime

# Tema
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Caminhos
CAMINHO_ANEXOS = "anexos"
CAMINHO_IMAGENS = "imagens"
ARQUIVO_CHAMADOS = "chamados.csv"

os.makedirs(CAMINHO_ANEXOS, exist_ok=True)
os.makedirs(CAMINHO_IMAGENS, exist_ok=True)

def carregar_imagem(nome_arquivo, tamanho):
    caminho = os.path.join(CAMINHO_IMAGENS, nome_arquivo)
    if os.path.exists(caminho):
        return customtkinter.CTkImage(light_image=Image.open(caminho), size=tamanho)
    return None

def salvar_chamado(nome, setor, data, descricao, imagem_caminho):
    with open(ARQUIVO_CHAMADOS, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([nome, setor, data, descricao, imagem_caminho])

def abrir_lista_chamados():
    janela_lista = customtkinter.CTkToplevel()
    janela_lista.title("Chamados Enviados")
    janela_lista.geometry("800x500")
    janela_lista.grid_columnconfigure(0, weight=1)
    janela_lista.grid_rowconfigure(0, weight=1)

    frame_tabela = customtkinter.CTkFrame(janela_lista)
    frame_tabela.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_tabela.grid_columnconfigure(0, weight=1)
    frame_tabela.grid_rowconfigure(0, weight=1)

    colunas = ("Nome", "Setor", "Data", "Descrição", "Imagem")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    if os.path.exists(ARQUIVO_CHAMADOS):
        with open(ARQUIVO_CHAMADOS, "r", encoding="utf-8") as f:
            for linha in csv.reader(f):
                tree.insert("", "end", values=linha)

def abrir_cadastro_chamado():
    janela_login.destroy()

    janela_chamado = customtkinter.CTk()
    janela_chamado.title("Cadastro de Chamado")
    janela_chamado.geometry("600x600")
    janela_chamado.grid_columnconfigure(0, weight=1)
    janela_chamado.grid_rowconfigure(0, weight=1)

    frame = customtkinter.CTkFrame(janela_chamado, corner_radius=20)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    customtkinter.CTkLabel(frame, text="Cadastro de Chamado", font=("Arial", 20)).pack(pady=20)

    entry_nome = customtkinter.CTkEntry(frame, placeholder_text="Seu nome")
    entry_nome.pack(pady=10, padx=30, fill="x")

    entry_setor = customtkinter.CTkEntry(frame, placeholder_text="Setor")
    entry_setor.pack(pady=10, padx=30, fill="x")

    entry_data = customtkinter.CTkEntry(frame, placeholder_text="Data (DD/MM/AAAA)")
    entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_data.pack(pady=10, padx=30, fill="x")

    text_descricao = customtkinter.CTkTextbox(frame, height=100)
    text_descricao.insert("0.0", "Descreva o problema...")
    text_descricao.pack(pady=10, padx=30, fill="x")

    imagem_anexada = {"caminho": ""}

    def selecionar_imagem():
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho:
            nome = os.path.basename(caminho)
            destino = os.path.join(CAMINHO_ANEXOS, nome)
            shutil.copy2(caminho, destino)
            imagem_anexada["caminho"] = destino
            messagebox.showinfo("Imagem", f"Imagem salva: {nome}")

    customtkinter.CTkButton(frame, text="Anexar Imagem", command=selecionar_imagem).pack(pady=10)

    def enviar_chamado():
        nome = entry_nome.get()
        setor = entry_setor.get()
        data = entry_data.get()
        descricao = text_descricao.get("0.0", "end").strip()
        imagem = imagem_anexada["caminho"]

        if nome and setor and data and descricao:
            salvar_chamado(nome, setor, data, descricao, imagem)
            messagebox.showinfo("Sucesso", "Chamado enviado!")
            janela_chamado.destroy()
            abrir_lista_chamados()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    customtkinter.CTkButton(frame, text="Enviar Chamado", command=enviar_chamado).pack(pady=20)
    customtkinter.CTkButton(frame, text="Ver Chamados", command=abrir_lista_chamados).pack()

    janela_chamado.mainloop()

def login():
    if entry_usuario.get() == "admin" and entry_senha.get() == "1234":
        abrir_cadastro_chamado()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

janela_login = customtkinter.CTk()
janela_login.geometry("800x400")
janela_login.title("Help Desk Cia do Terno")
janela_login.resizable(False, False)

janela_login.grid_columnconfigure((0, 1), weight=1)
janela_login.grid_rowconfigure(0, weight=1)

frame_esquerdo = customtkinter.CTkFrame(janela_login, corner_radius=20, fg_color="#2e2e2e")
frame_esquerdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

img1 = carregar_imagem("imagem1.png", (200, 100))
img2 = carregar_imagem("imagem2.png", (200, 100))

customtkinter.CTkLabel(frame_esquerdo, image=img1, text="").pack(pady=30) if img1 else customtkinter.CTkLabel(frame_esquerdo, text="Imagem1 faltando").pack(pady=30)
customtkinter.CTkLabel(frame_esquerdo, image=img2, text="").pack() if img2 else customtkinter.CTkLabel(frame_esquerdo, text="Imagem2 faltando").pack()

frame_direito = customtkinter.CTkFrame(janela_login, corner_radius=20, fg_color="#1e3a5f")
frame_direito.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

customtkinter.CTkLabel(frame_direito, text="Login", font=("Arial", 24)).pack(pady=20)
entry_usuario = customtkinter.CTkEntry(frame_direito, placeholder_text="Usuário")
entry_usuario.pack(pady=10, padx=30)
entry_senha = customtkinter.CTkEntry(frame_direito, placeholder_text="Senha", show="*")
entry_senha.pack(pady=10, padx=30)
customtkinter.CTkCheckBox(frame_direito, text="Lembrar-me").pack(pady=10)
customtkinter.CTkButton(frame_direito, text="Entrar", command=login).pack(pady=10)
customtkinter.CTkButton(frame_direito, text="Esqueci minha senha", fg_color="transparent", hover=False).pack()

janela_login.mainloop()
