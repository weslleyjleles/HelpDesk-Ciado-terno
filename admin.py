import customtkinter
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import platform
import subprocess

from util import carregar_chamados_sql, atualizar_status_chamado, salvar_resposta_chamado

def abrir_imagem_sistema(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.call(["open", path])
    else:
        subprocess.call(["xdg-open", path])

def abrir_admin(janela_pai=None):
    if janela_pai:
        janela_pai.withdraw()

    janela_admin = customtkinter.CTkToplevel() if janela_pai else customtkinter.CTk()
    janela_admin.title("Painel do Administrador")
    janela_admin.geometry("800x600")
    janela_admin.resizable(False, False)

    frame_topo = customtkinter.CTkFrame(janela_admin)
    frame_topo.pack(padx=10, pady=10, fill="x")

    status_var = customtkinter.StringVar(value="Todos")
    label_filtro = customtkinter.CTkLabel(frame_topo, text="Filtrar por status:")
    label_filtro.pack(side="left", padx=(0, 5))

    opcoes_status = ["Todos", "Aberto", "Fechado"]
    combo_status = customtkinter.CTkOptionMenu(frame_topo, values=opcoes_status, variable=status_var)
    combo_status.pack(side="left", padx=5)

    entry_busca = customtkinter.CTkEntry(frame_topo, placeholder_text="Buscar por texto...", width=300)
    entry_busca.pack(side="left", padx=5)

    def buscar():
        carregar_lista(filtro=entry_busca.get().strip(), status=status_var.get())

    customtkinter.CTkButton(frame_topo, text="Buscar", command=buscar).pack(side="left", padx=5)
    customtkinter.CTkButton(frame_topo, text="Atualizar", command=lambda: carregar_lista()).pack(side="left", padx=5)

    label_contador = customtkinter.CTkLabel(janela_admin, text="")
    label_contador.pack(pady=5)

    frame_chamados = customtkinter.CTkScrollableFrame(janela_admin, height=500)
    frame_chamados.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_lista(filtro="", status="Todos"):
        for widget in frame_chamados.winfo_children():
            widget.destroy()

        try:
            chamados = carregar_chamados_sql()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar chamados: {e}")
            return

        if filtro:
            chamados = [c for c in chamados if filtro.lower() in c.get("titulo", "").lower() or filtro.lower() in c.get("descricao", "").lower()]

        if status != "Todos":
            chamados = [c for c in chamados if c.get("status", "").lower() == status.lower()]

        label_contador.configure(text=f"Chamados encontrados: {len(chamados)}")

        for chamado in sorted(chamados, key=lambda x: x.get("data", ""), reverse=True):
            status_icone = "🟢" if chamado.get("status") == "Aberto" else "🔴"
            anexo = "📎" if chamado.get("anexo") else ""
            texto = f"{status_icone} {chamado.get('data', '')} | {chamado.get('usuario', '')} | {chamado.get('titulo', '')} | {chamado.get('status', '')} {anexo}"

            btn = customtkinter.CTkButton(
                frame_chamados,
                text=texto,
                anchor="w",
                command=lambda c=chamado: abrir_detalhes(c)
            )
            btn.pack(fill="x", pady=2)

    def abrir_detalhes(c):
        janela_detalhes = customtkinter.CTkToplevel(janela_admin)
        janela_detalhes.title("Detalhes do Chamado")
        janela_detalhes.geometry("600x700")
        janela_detalhes.lift()
        janela_detalhes.attributes("-topmost", True)
        janela_detalhes.after(10, lambda: janela_detalhes.attributes("-topmost", False))
        janela_detalhes.grab_set()

        usuario = str(c.get("usuario", "") or "")
        data = str(c.get("data", "") or "")
        descricao = str(c.get("descricao", "") or "")

        texto = f"Usuário: {usuario}\nData: {data}\n\nDescrição do Chamado:\n{descricao}"
        label_info = customtkinter.CTkLabel(janela_detalhes, text=texto, justify="left", anchor="w", wraplength=580)
        label_info.pack(padx=10, pady=10, fill="x")

        anexo_path = c.get("anexo", "")
        if anexo_path and os.path.exists(anexo_path):
            try:
                imagem = customtkinter.CTkImage(Image.open(anexo_path), size=(300, 200))
                img_label = customtkinter.CTkLabel(janela_detalhes, image=imagem, text="")
                img_label.image = imagem
                img_label.configure(cursor="hand2")
                img_label.pack(pady=10)
                img_label.bind("<Button-1>", lambda e: abrir_imagem_sistema(anexo_path))
            except Exception as e:
                messagebox.showwarning("Imagem", f"Erro ao carregar imagem: {e}")

        customtkinter.CTkLabel(janela_detalhes, text="Resposta do Administrador:", anchor="w").pack(padx=10, pady=(10, 2), fill="x")

        campo_resposta = customtkinter.CTkTextbox(janela_detalhes, height=200)
        campo_resposta.pack(padx=10, pady=5, fill="both", expand=True)

        resposta = str(c.get("resposta", "") or "")
        campo_resposta.insert("1.0", resposta)

        def salvar_resposta():
            salvar_resposta_chamado(c["id"], campo_resposta.get("1.0", "end").strip())
            messagebox.showinfo("Salvo", "Resposta salva com sucesso!")
            janela_detalhes.destroy()
            carregar_lista()

        def fechar_chamado():
            atualizar_status_chamado(c["id"], "Fechado")
            janela_detalhes.destroy()
            carregar_lista()

        def reabrir_chamado():
            atualizar_status_chamado(c["id"], "Aberto")
            janela_detalhes.destroy()
            carregar_lista()

        customtkinter.CTkButton(janela_detalhes, text="Salvar Resposta", command=salvar_resposta).pack(pady=5)

        if c.get("status") == "Aberto":
            customtkinter.CTkButton(janela_detalhes, text="Marcar como Fechado", command=fechar_chamado).pack(pady=5)
        elif c.get("status") == "Fechado":
            customtkinter.CTkButton(janela_detalhes, text="Reabrir Chamado", command=reabrir_chamado).pack(pady=5)

    carregar_lista()
    janela_admin.mainloop() if not janela_pai else None
