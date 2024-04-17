import pandas as pd
import requests

file_path = 'pedidos.xlsx'
products_df = pd.read_excel(file_path)

base_url = 'http://localhost:5000/'

def add_pedidos():
    url = f'{base_url}api/pedidos/add'
    headers = {'Content-Type': 'application/json'}

    for index, row in products_df.iterrows():
        payload = {
            'usuario_id': row['usuario_id'],
            'descricao': row['descricao'],
            'produtos': row['produtos'],
            'status': row['status']
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(f'Pedido "{row["usuario_id"]}" adicionado com sucesso.')
        else:
            print(f'Erro ao adicionar os pedidos "{row["usuario_id"]}". "{row["descricao"]}. "{row["produtos"]}. "{row["status"]}')

if __name__ == '__main__':
    add_pedidos()
