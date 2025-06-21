import json
from db import conectar

# Carrega os dados do arquivo JSON
with open('usuarios.json', encoding='utf-8') as f:
    dados = json.load(f)

# Conecta ao banco de dados
con = conectar()
cursor = con.cursor()

# Itera sobre os usuários no JSON e insere no banco
for nome, login in dados['clientes'].items():
    cursor.execute('''
        INSERT INTO Usuarios (nome, login, senha, tipo)
        VALUES (?, ?, ?, ?)
    ''', (nome, login, '1234', 'cliente'))  # senha e tipo são valores padrão aqui

# Salva e fecha
con.commit()
con.close()

print("✅ Usuários importados com sucesso.")
