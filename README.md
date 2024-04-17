------------------------------------------------------------------
# DOCUMENTAÇÃO DA API

Esta API foi desenvolvida para lidar com o registro e busca de usuários, assim como para gerenciar pedidos e produtos. Ela utiliza um banco de dados PostgreSQL para armazenamento de dados e oferece diversos endpoints para operações de CRUD e recuperação de dados.

## Tecnologias Utilizadas
•	Python
•	Flask
•	PostgreSQL

## Instruções de Configuração
## Configuração e Execução
1. Clone o repositório para sua máquina local:

```bash
git clone https://github.com/FabioMAmaral/cp2.git
```
2.	Instale o Python (caso ainda não esteja instalado)
3.	Instale os pacotes Python necessários:

pip install flask psycopg2 flasgger 

4.Configure o banco de dados PostgreSQL:
- Crie um banco de dados com o nome postgres
- Edite as variáveis de ambiente no arquivo .env com as informações do banco de dados:

DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=12345

Para a criação das tabelas é necessario o seguinte no script:
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

5.	Execute a aplicação Flask:

python app.py

6.	Acesse os endpoints da API utilizando ferramentas como Postman, cURL ou scripts.

------------------------------------------------------------------

# ENDPOINTS
  
### Usuários:
  •	Adicionar Usuário: POST /api/users/add
  
  •	Payload JSON:
  
  ```bash
    {
      "nome": "Nome do Usuário",
      "email": "usuario@example.com",
      "idade": 30
    } 
  ```

  •	Buscar Usuário: GET /api/users/<user_id>
  
  •	Parâmetros: ID do usuário a ser obtido
### Pedidos:
  •	Adicionar Pedido: POST /api/pedidos/add
  
  •	Payload JSON:
  
  ``` bash
   { 
   "usuario_id": 1 
   "descricao": "Descrição do Pedido" 
   "produtos": [1, 2, 3] 
   }
```
  •	Consultar Pedido: GET /api/pedidos/<pedido_id>
  
  •	Parâmetros: ID do pedido a ser obtido
  
Produtos:
  •	Adicionar Produto: POST /api/produtos/add
  
  •	Payload JSON: 
  
   ``` bash
   { 
   "nome": "Nome do Produto"
   "preco": 50.00 
   }
  ```
  •	Consultar Produto: GET /api/produtos/<produto_id>
  •	Parâmetros: ID do produto a ser obtido
  
------------------------------------------------------------------

#Scripts de Ingestão de Dados

Para popular as tabelas da API, siga os passos abaixo:
Na ordem para executar os scripts dessa ordem -> clientes_script.py -> produtos_script.py -> pedidos_script.py
(Pois nessa ordem ao finalizar a tabela pedidos_produtos vai fazer a alto incrementação dos ids dos pedidos e os ids dos produtos)

##Adicionar Produtos
1. Coloque o arquivo de produtos no formato TXT, CSV, XLSX ou JSON dentro do diretório ingestao-de-dados.
2. Execute o script produtos_script.py para adicionar os produtos à API:

python ingestao-de-dados/produtos_script.py

#Adicionar Clientes
1. Coloque o arquivo de clientes no formato TXT, CSV, XLSX ou JSON dentro do diretório ingestao-de-dados.
2. Execute o script clientes_script.py para adicionar os clientes à API:

python ingestao-de-dados/clientes_script.py

#Criar Pedidos

1. Execute o script pedidos_script.py para criar pedidos usando os IDs de clientes e produtos já cadastrados:
   
python ingestao-de-dados/pedidos_script.py

Certifique-se de que os arquivos de dados estejam formatados corretamente e sigam as regras estabelecidas na API.
------------------------------------------------------------------

# TESTES
Você pode testar a API utilizando ferramentas como Postman, cURL ou escrevendo scripts para interagir com os endpoints. Certifique-se de fornecer dados válidos nos payloads das requisições para operações bem-sucedidas.
