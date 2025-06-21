import json
from datetime import datetime
from db import conectar

# Mapeamento de cliente
clientes = {
    "Dp": "dp01",
    "Dp02": "dp02"
}

# Carrega o JSON
with open('chamados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Conecta ao banco
con = conectar()
cursor = con.cursor()

for chamado in dados['chamados']:
    data_formatada = datetime.strptime(chamado['data'], "%d/%m/%Y %H:%M")
    cliente_codigo = clientes.get(chamado['usuario'], "desconhecido")

    cursor.execute('''
        INSERT INTO Chamados (
            usuario, nome, setor, data, anexo, descricao, status, resposta, cliente_codigo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        chamado['usuario'],
        chamado['nome'],
        chamado['setor'],
        data_formatada,
        chamado['anexo'],
        chamado['descricao'],
        chamado['status'],
        chamado['resposta'],
        cliente_codigo
    ))

con.commit()
con.close()

print("✅ Chamados importados com sucesso!")
