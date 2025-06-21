import customtkinter
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from util import salvar_chamado_sql, carregar_chamados_sql


def abrir_cliente(usuario):
    janela_cliente = customtkinter.CTk()
    janela_cliente.title("Painel do Cliente")
    janela_cliente.geometry("800x700")
    janela_cliente.resizable(False, False)

    frame_principal = customtkinter.CTkFrame(janela_cliente)
    frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

    label_titulo = customtkinter.CTkLabel(frame_principal, text="Abrir Chamado", font=("Arial", 18))
    label_titulo.pack(pady=10)

    entry_titulo = customtkinter.CTkEntry(frame_principal, placeholder_text="Título do Chamado", width=400)
    entry_titulo.pack(pady=5)

    entry_setor = customtkinter.CTkEntry(frame_principal, placeholder_text="Setor", width=400)
    entry_setor.pack(pady=5)

    campo_descricao = customtkinter.CTkTextbox(frame_principal, height=150, width=600)
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
    btn_anexo.pack(pady=2)

    def enviar_chamado():
        titulo = entry_titulo.get().strip()
        setor = entry_setor.get().strip()
        descricao = campo_descricao.get("1.0", "end").strip()

        if not titulo or not setor or not descricao:
            messagebox.showwarning("Campos obrigatórios", "Preencha o título, setor e a descrição.")
            return

        try:
            salvar_chamado_sql(titulo, descricao, caminho_imagem, usuario)
            messagebox.showinfo("Chamado enviado", "Seu chamado foi enviado com sucesso.")
            entry_titulo.delete(0, "end")
            entry_setor.delete(0, "end")
            campo_descricao.delete("1.0", "end")
            campo_descricao.insert("1.0", "Descreva o problema aqui...")
            label_anexo.configure(text="Nenhuma imagem selecionada")
            carregar_historico()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar chamado: {e}")

    btn_enviar = customtkinter.CTkButton(frame_principal, text="Enviar Chamado", command=enviar_chamado)
    btn_enviar.pack(pady=2)

    frame_filtros = customtkinter.CTkFrame(frame_principal, fg_color="transparent")
    frame_filtros.pack(pady=10)

    entry_busca = customtkinter.CTkEntry(frame_filtros, placeholder_text="Buscar chamados...", width=180)
    entry_busca.pack(side="left", padx=5)

    status_var = customtkinter.StringVar(value="Todos")
    filtro_status = customtkinter.CTkComboBox(frame_filtros, values=["Todos", "Aberto", "Fechado"], variable=status_var, width=100)
    filtro_status.pack(side="left", padx=5)

    def buscar_chamados():
        termo = entry_busca.get().strip().lower()
        status = status_var.get()
        carregar_historico(filtro=termo, status=status)

    btn_buscar = customtkinter.CTkButton(frame_filtros, text="Buscar", command=buscar_chamados)
    btn_buscar.pack(side="left", padx=5)

    label_historico = customtkinter.CTkLabel(frame_principal, text="Seus Chamados", font=("Arial", 16))
    label_historico.pack(pady=10)

    frame_historico = customtkinter.CTkScrollableFrame(frame_principal, height=250)
    frame_historico.pack(fill="both", expand=True)

    def carregar_historico(filtro="", status="Todos"):
        for widget in frame_historico.winfo_children():
            widget.destroy()

        try:
            chamados = carregar_chamados_sql()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar chamados: {e}")
            return

        chamados_usuario = [c for c in chamados if c[6] == usuario]

        chamados_dict = [{
            "id": c[0],
            "titulo": c[1],
            "descricao": c[2],
            "anexo": c[3],
            "data": str(c[4])[:16],
            "status": c[5],
            "usuario": c[6],
            "resposta": c[7] if len(c) > 7 else ""
        } for c in chamados_usuario]

        if filtro:
            chamados_dict = [c for c in chamados_dict if filtro in c["titulo"].lower() or filtro in c["descricao"].lower()]

        if status != "Todos":
            chamados_dict = [c for c in chamados_dict if c["status"] == status]

        if not chamados_dict:
            label_vazio = customtkinter.CTkLabel(frame_historico, text="Nenhum chamado encontrado.")
            label_vazio.pack()
            return

        for chamado in chamados_dict[::-1]:
            texto = f"Título: {chamado['titulo']}\n" \
                    f"Data: {chamado['data']}\n" \
                    f"Descrição: {chamado['descricao']}\n" \
                    f"Status: {chamado['status']}\n" \
                    f"Resposta: {chamado['resposta'] or 'Aguarde resposta do administrador'}"

            frame_chamado = customtkinter.CTkFrame(frame_historico)
            frame_chamado.pack(pady=5, padx=10, fill="x", expand=True)

            label_chamado = customtkinter.CTkLabel(
                frame_chamado,
                text=texto,
                anchor="w",
                justify="left",
                wraplength=680
            )
            label_chamado.pack(padx=10, pady=5, anchor="w")

            if chamado["anexo"] and os.path.exists(chamado["anexo"]):
                imagem = customtkinter.CTkImage(Image.open(chamado["anexo"]), size=(100, 100))
                img_label = customtkinter.CTkLabel(frame_chamado, image=imagem, text="")
                img_label.image = imagem
                img_label.pack(pady=5, padx=10)

                def abrir_imagem(caminho=chamado["anexo"]):
                    nova = customtkinter.CTkToplevel(janela_cliente)
                    nova.title("Imagem Anexada")
                    nova.geometry("600x600")
                    nova.lift()
                    nova.attributes("-topmost", True)
                    nova.after(10, lambda: nova.attributes("-topmost", False))
                    nova.grab_set()

                    img = Image.open(caminho)
                    img.thumbnail((580, 580))
                    img_tk = ImageTk.PhotoImage(img)
                    lbl = customtkinter.CTkLabel(nova, image=img_tk, text="")
                    lbl.image = img_tk
                    lbl.pack(padx=10, pady=10)

                img_label.bind("<Button-1>", lambda e, caminho=chamado["anexo"]: abrir_imagem(caminho))

    carregar_historico()
    janela_cliente.mainloop()
