import customtkinter
from tkinter import messagebox
from util import carregar_chamados, salvar_chamados
import os
from PIL import Image, ImageTk
import tkinter as tk
from customtkinter import CTkImage

# Função para abrir imagem ampliada
def abrir_imagem_ampliada(caminho_imagem):
    nova_janela = tk.Toplevel()
    nova_janela.title("Imagem Ampliada")
    nova_janela.state("zoomed")
    nova_janela.configure(background="black")

    canvas = tk.Canvas(nova_janela, bg="black")
    scrollbar_y = tk.Scrollbar(nova_janela, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(nova_janela, orient="horizontal", command=canvas.xview)
    frame_imagem = tk.Frame(canvas, bg="black")

    frame_imagem.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_imagem, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    img = Image.open(caminho_imagem)
    largura_tela = nova_janela.winfo_screenwidth()
    altura_tela = nova_janela.winfo_screenheight()
    img.thumbnail((largura_tela * 0.95, altura_tela * 0.95), Image.LANCZOS)

    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(frame_imagem, image=img_tk, bg="black")
    label_img.image = img_tk
    label_img.pack(padx=10, pady=10)

    tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy, bg="#333", fg="white").pack(pady=10)

# Função principal do painel admin
def abrir_admin():
    janela_admin = customtkinter.CTk()
    janela_admin.title("Painel do Administrador")
    janela_admin.geometry("800x600")
    janela_admin.resizable(False, False)

    frame_principal = customtkinter.CTkFrame(janela_admin)
    frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

    frame_topo = customtkinter.CTkFrame(frame_principal)
    frame_topo.pack(fill="x")

    label_filtro = customtkinter.CTkLabel(frame_topo, text="Filtrar por status:")
    label_filtro.pack(side="left", padx=10)

    frame_lista = customtkinter.CTkFrame(frame_principal)
    frame_lista.pack(fill="both", expand=True, pady=10)

    lista_chamados = customtkinter.CTkScrollableFrame(frame_lista)
    lista_chamados.pack(padx=10, pady=10, fill="both", expand=True)

    chamados = carregar_chamados()

    def atualizar_lista_chamados(widget_lista, chamados, status):
        for widget in widget_lista.winfo_children():
            widget.destroy()

        encontrados = 0
        for i, chamado in enumerate(chamados):
            if status != "Todos" and chamado.get("status", "Aberto") != status:
                continue
            encontrados += 1
            texto = f"{chamado.get('data', '')} | {chamado.get('nome', '')} | {chamado.get('setor', '')} | {chamado.get('status', '')}"
            btn = customtkinter.CTkButton(widget_lista, text=texto, anchor="w", width=700,
                                          command=lambda i=i: visualizar_chamado(chamados[i], chamados, i, janela_admin))
            btn.pack(pady=5, padx=5)

        if encontrados == 0:
            customtkinter.CTkLabel(widget_lista, text="Nenhum chamado encontrado.").pack(pady=20)

    def visualizar_chamado(chamado, chamados, indice, janela_principal):
        janela = customtkinter.CTkToplevel(janela_principal)
        janela.title("Visualizar Chamado")
        janela.geometry("500x600")
        janela.resizable(False, False)
        janela.transient(janela_principal)
        janela.grab_set()
        janela.focus_force()

        info = (
            f"Nome: {chamado.get('nome', '')}\n"
            f"Setor: {chamado.get('setor', '')}\n"
            f"Data: {chamado.get('data', '')}\n"
            f"\nDescrição:\n"
        )

        customtkinter.CTkLabel(janela, text=info, justify="left", anchor="w", wraplength=480).pack(pady=5, padx=10)
        customtkinter.CTkLabel(janela, text=chamado.get("descricao", "Sem descrição"), justify="left", anchor="w", wraplength=480).pack(padx=10)

        if chamado.get("anexo"):
            caminho_anexo = os.path.normpath(chamado["anexo"])
            caminho_completo = os.path.join(os.getcwd(), caminho_anexo)

            if os.path.exists(caminho_completo):
                imagem = CTkImage(light_image=Image.open(caminho_completo), size=(200, 200))
                label_imagem = customtkinter.CTkLabel(janela, image=imagem, text="")
                label_imagem.image = imagem
                label_imagem.pack(pady=5)

                def abrir_imagem_com_foco(janela_atual, caminho):
                    janela_atual.grab_release()
                    abrir_imagem_ampliada(caminho)

                label_imagem.bind("<Button-1>", lambda e: abrir_imagem_com_foco(janela, caminho_completo))
            else:
                print(f"[ERRO] Anexo não encontrado: {caminho_completo}")

        if chamado.get("resposta"):
            customtkinter.CTkLabel(
                janela,
                text=f"\nResposta anterior:\n{chamado['resposta']}",
                text_color="green",
                anchor="w",
                wraplength=480
            ).pack(padx=10)

        campo_resposta = customtkinter.CTkTextbox(janela, height=100)
        campo_resposta.pack(pady=10, padx=10)

        def responder():
            resposta = campo_resposta.get("1.0", "end").strip()
            if resposta:
                chamado["resposta"] = resposta
                chamado["status"] = "Fechado"
                salvar_chamados(chamados)
                atualizar_lista_chamados(lista_chamados, chamados, status_filtro.get())
                messagebox.showinfo("Sucesso", "Chamado respondido e fechado.")
                janela.destroy()
            else:
                messagebox.showwarning("Aviso", "Digite uma resposta antes de enviar.")

        customtkinter.CTkButton(janela, text="Responder e Fechar", command=responder).pack(pady=10)

    status_filtro = customtkinter.CTkOptionMenu(
        frame_topo, values=["Todos", "Aberto", "Fechado"],
        command=lambda s: atualizar_lista_chamados(lista_chamados, chamados, s)
    )
    status_filtro.set("Todos")
    status_filtro.pack(side="left", padx=10)

    atualizar_lista_chamados(lista_chamados, chamados, "Todos")

    janela_admin.mainloop()
