✅ README.md para o projeto Help Desk - Cia do Terno
markdown
# 🛠️ Help Desk - Cia do Terno

Sistema de Help Desk desenvolvido em Python com interface gráfica usando [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) e banco de dados SQLite.

## 📌 Funcionalidades

- Login de usuários (cliente e administrador)
- Clientes podem:
  - Abrir chamados com título, setor, descrição e anexo de imagem
  - Acompanhar o histórico de chamados, com filtros e buscas
- Administradores podem:
  - Visualizar todos os chamados
  - Filtrar por status (Aberto / Fechado)
  - Responder chamados
  - Marcar chamados como fechados ou reabri-los

## 🧰 Tecnologias Utilizadas

- Python 3.11+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Pillow (para manipulação de imagens)
- SQLite (banco de dados local)

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/HelpDesk-CiaDoTerno.git
cd HelpDesk-CiaDoTerno
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Caso não tenha um requirements.txt, crie com:
pip freeze > requirements.txt

▶️ Execução
Rode o arquivo principal:

bash
Copiar
Editar
python main.py
🗃️ Estrutura do Projeto
bash
Copiar
Editar
HelpDesk-CiaDoTerno/
│
├── cliente.py         # Painel do cliente
├── admin.py           # Painel do administrador
├── login.py           # Tela de login
├── main.py            # Janela inicial
├── db.py              # Conexão e criação do banco SQLite
├── util.py            # Funções auxiliares
├── imagens/           # Imagens usadas no sistema
├── anexos/            # Imagens anexadas aos chamados
├── chamados.db        # Banco de dados SQLite
└── README.md
🔒 Login de Teste
Usuário cliente: cliente1 / senha123

Usuário admin: admin1 / admin123

Esses dados podem estar no banco ou arquivo de usuários, conforme sua implementação.

📌 Observações
O sistema funciona localmente, ideal para pequenas empresas.

Imagens anexadas são abertas com clique no thumbnail.

👨‍💻 Autor
Weslley J. Leles – Desenvolvedor Python
📝 Licença
Este projeto é de uso interno. Entre em contato com o autor para mais informações.
