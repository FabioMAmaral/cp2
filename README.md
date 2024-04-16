------------------------------------------------------------------
DOCUMENTAÇÃO DA API

Esta API foi desenvolvida para lidar com o registro e busca de usuários, assim como para gerenciar pedidos e produtos. Ela utiliza um banco de dados PostgreSQL para armazenamento de dados e oferece diversos endpoints para operações de CRUD e recuperação de dados.

------------------------------------------------------------------
Tecnologias Utilizadas
•	Python
•	Flask
•	PostgreSQL

Instruções de Configuração
1.	Clone o repositório do GitHub: [(https://github.com/FabioMAmaral/cp2.git)]
2.	Instale o Python (caso ainda não esteja instalado)
3.	Instale os pacotes Python necessários:

pip install flask psycopg2 flasgger 

4.	Configure o seu banco de dados PostgreSQL e atualize as credenciais do banco de dados no código (db_host, db_name, db_user, db_password).
5.	Execute a aplicação Flask:
   
python app.py 
7.	Acesse os endpoints da API utilizando ferramentas como Postman, cURL ou scripts.
   
ENDPOINTS
Usuários:
  •	Adicionar Usuário: POST /api/users/add
  •	Payload JSON: { "nome": "Nome do Usuário", "email": "email@example.com", "idade": 30 }
  •	Buscar Usuário: GET /api/users/<user_id>
  •	Parâmetros: ID do usuário a ser obtido
Pedidos:
  •	Adicionar Pedido: POST /api/pedidos/add
  •	Payload JSON: { "usuario_id": 1, "descricao": "Descrição do Pedido", "produtos": [1, 2, 3] }
  •	Consultar Pedido: GET /api/pedidos/<pedido_id>
  •	Parâmetros: ID do pedido a ser obtido
Produtos:
  •	Adicionar Produto: POST /api/produtos/add
  •	Payload JSON: { "nome": "Nome do Produto", "preco": 50.00 }
  •	Consultar Produto: GET /api/produtos/<produto_id>
  •	Parâmetros: ID do produto a ser obtido
  
Para mais detalhes sobre cada endpoint, incluindo os dados necessários nos payloads das requisições e o formato das respostas, consulte a documentação do Swagger fornecida no código da API.

TESTES
Você pode testar a API utilizando ferramentas como Postman, cURL ou escrevendo scripts para interagir com os endpoints. Certifique-se de fornecer dados válidos nos payloads das requisições para operações bem-sucedidas.
