import customtkinter
from tkinter import messagebox, simpledialog
import json
from admin import abrir_admin
from cliente import abrir_cliente

class LoginApp:
    ARQUIVO_USUARIOS = "usuarios.json"

    def __init__(self, frame_pai, janela_login):
        self.frame_pai = frame_pai
        self.janela_login = janela_login
        self.usuarios_clientes = self.carregar_usuarios()
        self.criar_interface()

    def carregar_usuarios(self):
        try:
            with open(self.ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return dados.get("clientes", {})
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Erro ao ler o arquivo JSON.")
            return {}

    def salvar_usuarios(self):
        dados = {"clientes": self.usuarios_clientes}
        try:
            with open(self.ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")

    def criar_interface(self):
        # Limpa frame
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

        if usuario == "admin" and senha == "1234":
            self.janela_login.destroy()
            abrir_admin()
        elif usuario in self.usuarios_clientes and self.usuarios_clientes[usuario] == senha:
            self.janela_login.destroy()
            abrir_cliente(usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def cadastrar_cliente(self):
        usuario_novo = simpledialog.askstring("Cadastro", "Digite o nome de usuário:")
        if not usuario_novo:
            return

        if usuario_novo in self.usuarios_clientes:
            messagebox.showwarning("Aviso", "Usuário já existe!")
            return

        senha_nova = simpledialog.askstring("Cadastro", "Digite a senha:", show="*")
        if not senha_nova:
            return

        self.usuarios_clientes[usuario_novo] = senha_nova
        self.salvar_usuarios()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

def abrir_login(frame_direito, janela_login):
    LoginApp(frame_direito, janela_login)
