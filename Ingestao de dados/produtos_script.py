import pandas as pd
import requests

file_path = 'produtos.xlsx'
products_df = pd.read_excel(file_path)

base_url = 'http://localhost:5000/'

def add_produtos():
    url = f'{base_url}api/produtos/add'
    headers = {'Content-Type': 'application/json'}

    for index, row in products_df.iterrows():
        payload = {
            'nome': row['nome'],
            'preco': row['preco']
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(f'Produto "{row["nome"]}" adicionado com sucesso.')
        else:
            print(f'Erro ao adicionar os produtos "{row["nome"]}". "{row["preco"]}')

if __name__ == '__main__':
    add_produtos()
