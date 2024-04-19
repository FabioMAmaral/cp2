# DOCUMENTAÇÃO DA API

Esta API foi desenvolvida para lidar com o registro e busca de usuários, bem como para gerenciar pedidos e produtos. Ela utiliza um banco de dados PostgreSQL para armazenamento de dados e oferece diversos endpoints para operações de CRUD e recuperação de dados.

## Tecnologias Utilizadas

- Python
- Flask
- PostgreSQL
- DBeaver (Para visualizar os dados que foram adicionados pela API app.py e os scripts)

## Instruções de Configuração

### Configuração e Execução

1. Clone o repositório para sua máquina local:

git clone https://github.com/FabioMAmaral/cp2.git

2. Instale o Python (caso ainda não esteja instalado).
3. Instale os pacotes Python necessários:

pip install flask psycopg2 flasgger

4. Configure o banco de dados PostgreSQL:
- Crie um banco de dados com o nome “postgres”.
- Edite as variáveis de ambiente no arquivo .env com as informações do banco de dados:

  ```
  DB_HOST=localhost
  DB_NAME=postgres
  DB_USER=postgres
  DB_PASSWORD=12345
  ```

5. Para a criação das tabelas, execute o seguinte script SQL:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    idade INT
);
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco NUMERIC(10, 2) NOT NULL
);
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES users(id),
    descricao TEXT,
    status VARCHAR(50)
);
CREATE TABLE pedidos_produtos (
    pedido_id INT REFERENCES pedidos(id),
    produto_id INT REFERENCES produtos(id),
    PRIMARY KEY (pedido_id, produto_id)
);
 ```
6. Execute a aplicação Flask:

python app.py

7. Acesse os endpoints da API utilizando ferramentas como Postman, cURL ou scripts.

## ENDPOINTS

### Usuários:
- Adicionar Usuário: POST /api/users/add
    - Payload JSON:
  ```
  {
  "nome": "Nome do Usuário",
  "email": "usuario@example.com",
  "idade": 30
  }
  ```
- Buscar Usuário: GET /api/users/<user_id>
    - Parâmetros: ID do usuário a ser obtido

### Produtos:
- Adicionar Produto: POST /api/produtos/add
    - Payload JSON:
   ```
  {
   "nome": "Nome do produto",
   "preco": "Preço do produto"
   }
   ```
- Buscar produtos: GET /api/produtos/<produto_id>
    - Parâmetros: ID do produto a ser obtido

### Pedidos:
- Adicionar Pedido: POST /api/pedidos/add
    - Payload JSON:
   ```
  {
   "usuario_id": 1,
   "descricao": "Descrição do Pedido",
   "produtos": [1, 2, 3]
   }
   ```
- Buscar pedidos: GET /api/pedidos/<pedidos_id>
    - Parâmetros: ID do pedido a ser obtido

--------------------------------------------------------------------------------
# Scripts de Ingestão de Dados
Para popular as tabelas da API.
Lembrando que o app.py tem que estar rodando simultaneamente com os scripts e os arquivos em formato .xlsx seguindo os passos abaixo:

## Adicionar Clientes
1. Coloque o arquivo de clientes no formato XLSX dentro do diretório ingestao-de-dados.
2. Execute o script clientes_script.py para adicionar os produtos à API:

python clientes_script.py

## Adicionar Produtos
1. Coloque o arquivo de produtos no formato XLSX dentro do diretório ingestao-de-dados.
2. Execute o script produtos_script.py para adicionar os produtos à API:

python produtos_scripty.py

## Adicionar Pedidos
1. Coloque o arquivo de pedidos no formato XLSX dentro do diretório ingestao-de-dados.
2. Execute o script pedidos_script.py para adicionar os produtos à API:

python pedidos_script.py

Assim populando as tabelas com os scripts.
