import customtkinter
import os
import json
import datetime
from tkinter import filedialog, messagebox
from util import salvar_chamados, carregar_chamados

def abrir_cliente(usuario):
    janela_cliente = customtkinter.CTk()
    janela_cliente.title("Painel do Cliente")
    janela_cliente.geometry("800x600")
    janela_cliente.resizable(False, False)

    frame_principal = customtkinter.CTkFrame(janela_cliente)
    frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

    label_titulo = customtkinter.CTkLabel(frame_principal, text="Abrir Chamado", font=("Arial", 18))
    label_titulo.pack(pady=10)

    entry_setor = customtkinter.CTkEntry(frame_principal, placeholder_text="Setor")
    entry_setor.pack(pady=5)

    campo_descricao = customtkinter.CTkTextbox(frame_principal, height=100)
    campo_descricao.pack(pady=5)
    campo_descricao.insert("1.0", "Descreva o problema aqui...")

    label_anexo = customtkinter.CTkLabel(frame_principal, text="Nenhuma imagem selecionada")
    label_anexo.pack(pady=5)

    caminho_imagem = None

    def selecionar_imagem():
        nonlocal caminho_imagem
        arquivo = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if arquivo:
            caminho_imagem = arquivo
            label_anexo.configure(text=os.path.basename(arquivo))

    btn_anexo = customtkinter.CTkButton(frame_principal, text="Selecionar Imagem", command=selecionar_imagem)
    btn_anexo.pack(pady=5)

    def enviar_chamado():
        setor = entry_setor.get().strip()
        descricao = campo_descricao.get("1.0", "end").strip()

        if not setor or not descricao:
            messagebox.showwarning("Campos obrigatórios", "Preencha o setor e a descrição.")
            return

        chamados = carregar_chamados()

        novo_chamado = {
            "usuario": usuario,
            "nome": usuario,
            "setor": setor,
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "anexo": caminho_imagem,
            "descricao": descricao,
            "status": "Aberto",
            "resposta": ""
        }

        chamados.append(novo_chamado)
        salvar_chamados(chamados)

        messagebox.showinfo("Chamado enviado", "Seu chamado foi enviado com sucesso.")
        entry_setor.delete(0, "end")
        campo_descricao.delete("1.0", "end")
        label_anexo.configure(text="Nenhuma imagem selecionada")

    btn_enviar = customtkinter.CTkButton(frame_principal, text="Enviar Chamado", command=enviar_chamado)
    btn_enviar.pack(pady=10)

    janela_cliente.mainloop()
