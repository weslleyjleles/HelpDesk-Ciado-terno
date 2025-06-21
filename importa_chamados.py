from db import conectar
import json
from datetime import datetime

# Abrir os arquivos JSON
with open('chamados.json', encoding='utf-8') as f:
    dados = json.load(f)

with open('usuarios.json', encoding='utf-8') as f:
    clientes = json.load(f)['clientes']

# Conectar no banco
con = conectar()
cursor = con.cursor()

for chamado in dados['chamados']:
    data_formatada = datetime.strptime(chamado['data'], "%d/%m/%Y %H:%M")
    cliente_codigo = clientes.get(chamado['usuario'], "desconhecido")

    cursor.execute('''
        INSERT INTO Chamados (usuario, titulo, descricao, imagem_path, data_abertura, status, cliente_codigo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        chamado['usuario'],
        chamado['nome'],  # 'nome' será mapeado para 'titulo'
        chamado['descricao'],
        chamado['anexo'],
        data_formatada,
        chamado['status'],
        cliente_codigo
    ))

con.commit()
con.close()
print("✅ Chamados importados com sucesso.")
