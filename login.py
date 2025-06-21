import customtkinter
from tkinter import messagebox, simpledialog
import sqlite3
from admin import abrir_admin
from cliente import abrir_cliente
from db import conectar

class LoginApp:
    def __init__(self, frame_pai, janela_login):
        self.frame_pai = frame_pai
        self.janela_login = janela_login
        self.criar_interface()

    def criar_interface(self):
        for widget in self.frame_pai.winfo_children():
            widget.destroy()

        customtkinter.CTkLabel(self.frame_pai, text="Login", font=("Arial", 24)).pack(pady=20)

        self.entry_usuario = customtkinter.CTkEntry(self.frame_pai, placeholder_text="Usuário")
        self.entry_usuario.pack(pady=10, padx=30)

        self.entry_senha = customtkinter.CTkEntry(self.frame_pai, placeholder_text="Senha", show="*")
        self.entry_senha.pack(pady=10, padx=30)

        customtkinter.CTkButton(self.frame_pai, text="Entrar", command=self.login).pack(pady=10)
        customtkinter.CTkButton(self.frame_pai, text="Cadastrar Cliente", command=self.cadastrar_cliente).pack(pady=5)
        customtkinter.CTkButton(self.frame_pai, text="Esqueci minha senha", fg_color="transparent", hover=False).pack()

    def login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT tipo FROM Usuarios WHERE login=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            tipo = resultado[0]
            if tipo == "admin":
                self.janela_login.after(100, lambda: (self.janela_login.withdraw(), abrir_admin(self.janela_login)))
            else:
                self.janela_login.after(100, lambda: (self.janela_login.destroy(), abrir_cliente(usuario)))
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def cadastrar_cliente(self):
        usuario_novo = simpledialog.askstring("Cadastro", "Digite o nome de usuário:")
        if not usuario_novo:
            return

        senha_nova = simpledialog.askstring("Cadastro", "Digite a senha:", show="*")
        if not senha_nova:
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Usuarios WHERE login = ?", (usuario_novo,))
        if cursor.fetchone():
            conn.close()
            messagebox.showwarning("Aviso", "Usuário já existe!")
            return

        cursor.execute("INSERT INTO Usuarios (nome, login, senha, tipo) VALUES (?, ?, ?, ?)", (usuario_novo, usuario_novo, senha_nova, "cliente"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

def abrir_login(frame_direito, janela_login):
    LoginApp(frame_direito, janela_login)
