import customtkinter
from login import abrir_login
from util import carregar_imagem  # Supondo que essa função carrega imagem com PIL + ImageTk

# Configurações visuais
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Criação da janela principal
janela_login = customtkinter.CTk()
janela_login.geometry("800x400")
janela_login.title("Help Desk Cia do Terno")
janela_login.resizable(False, False)

# Organização em grid (2 colunas)
janela_login.grid_columnconfigure((0, 1), weight=1)
janela_login.grid_rowconfigure(0, weight=1)

# Frame esquerdo - Imagens
frame_esquerdo = customtkinter.CTkFrame(janela_login, corner_radius=20, fg_color="#2e2e2e")
frame_esquerdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Carregar e exibir imagens no frame esquerdo
img1 = carregar_imagem("imagem1.jpg", (300, 150))
img2 = carregar_imagem("imagem2.png", (300, 100))

if img1:
    label1 = customtkinter.CTkLabel(frame_esquerdo, image=img1, text="")
    label1.image = img1  # <- Evita o garbage collector remover a imagem
    label1.pack(pady=10)

if img2:
    label2 = customtkinter.CTkLabel(frame_esquerdo, image=img2, text="")
    label2.image = img2
    label2.pack(pady=10)

# Frame direito - Formulário de login
frame_direito = customtkinter.CTkFrame(janela_login, corner_radius=20, fg_color="#1e3a5f")
frame_direito.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# Abre o formulário de login dentro do frame direito
abrir_login(frame_direito, janela_login)

# Loop da janela
janela_login.mainloop()
print("Interface principal carregada com sucesso.")