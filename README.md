# 🛠️ Help Desk - Cia do Terno

Sistema de Help Desk desenvolvido em Python com interface gráfica utilizando [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

## 🎯 Funcionalidades

- Autenticação de usuários com login e senha
- Dois tipos de usuários: `cliente` e `admin`
- Clientes podem:
  - Abrir chamados com: título, setor, descrição, data e anexo de imagem
  - Visualizar o histórico de chamados enviados
- Administradores podem:
  - Visualizar todos os chamados
  - Filtrar por status: Aberto / Fechado
  - Visualizar anexos clicando para abrir em tela cheia
  - Responder chamados e marcar como fechados

---

## 🧰 Tecnologias

- Python 3.10+
- CustomTkinter
- Pillow (PIL)
- JSON (armazenamento local)
- Estrutura modular em arquivos: `login.py`, `admin.py`, `cliente.py`, `util.py`

---

## 🚀 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/weslleyjleles/HelpDesk-Ciado-terno.git
cd HelpDesk-Ciado-terno
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute o sistema:

bash
Copiar
Editar
python main.py
🧾 Estrutura de Pastas
pgsql
Copiar
Editar
HelpDesk/
├── main.py
├── login.py
├── admin.py
├── cliente.py
├── util.py
├── chamados.json
├── usuarios.json
├── anexos/
├── imagens/
└── README.md


🔐 Tipos de Usuários
O sistema possui dois perfis:

Tipo	Função
admin	Gerencia chamados de todos os clientes
cliente	Abre e acompanha seus próprios chamados

As credenciais são armazenadas em usuarios.json.

📦 Gerar Executável (Opcional)
Você pode usar pyinstaller para criar um .exe:

bash
Copiar
Editar
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed main.py
🧑‍💻 Autor
Weslley Leles
Projeto desenvolvido para uso interno da empresa Cia do Terno.

📝 Licença
Este projeto é de uso interno. Entre em contato com o autor para mais informações.
