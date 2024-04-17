import pandas as pd
import requests

file_path = 'clientes.xlsx'
products_df = pd.read_excel(file_path)

base_url = 'http://localhost:5000/'

def add_users():
    url = f'{base_url}api/users/add'
    headers = {'Content-Type': 'application/json'}

    for index, row in products_df.iterrows():
        payload = {
            'nome': row['nome'],
            'email': row['email'],
            'idade': row['idade']
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(f'Usuarios "{row["nome"]}" adicionado com sucesso.')
        else:
            print(f'Erro ao adicionar os usuarios "{row["nome"]}". "{row["email"]}". "{row["idade"]}" ' )

if __name__ == '__main__':
    add_users()
