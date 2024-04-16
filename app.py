from flask import Flask, jsonify, request
from flasgger import Swagger
import psycopg2

db_host = 'localhost'
db_name = 'postgres'
db_user = 'postgres'
db_password = '12345'

conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    List all users
    ---
    responses:
      200:
        description: A list of users
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the user to get
    responses:
      200:
        description: Details of the user
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return jsonify(user)

@app.route('/api/users/add', methods=['POST'])
def add_user():
    """
    Add a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - nome
            - email
            - idade
          properties:
            nome:
              type: string
              description: Name of the user
            email:
              type: string
              description: Email of the user
            idade:
              type: integer
              description: Age of the user
    responses:
      201:
        description: User added successfully
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    idade = data.get('idade')

    if nome is None or email is None or idade is None:
        return jsonify({'message': 'Erro: Todos os campos (nome, email, idade) são obrigatórios.'}), 400

    if not isinstance(idade, int) or idade <= 0:
        return jsonify({'message': 'Erro: Idade deve ser um número inteiro positivo.'}), 400
    
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (nome, email, idade) VALUES (%s, %s, %s)', (nome, email, idade))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Usuário adicionado com sucesso.'}), 201

@app.route('/api/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the user to update
      - name: body
        in: body
        required: true
        schema:
          id: UserUpdate
          properties:
            nome:
              type: string
              description: Updated name of the user
            email:
              type: string
              description: Updated email of the user
            idade:
              type: integer
              description: Updated age of the user
    responses:
      200:
        description: User updated successfully
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    idade = data.get('idade')

    if nome is None or email is None or idade is None:
        return jsonify({'message': 'Erro: Todos os campos (nome, email, idade) são obrigatórios.'}), 400

    if not isinstance(idade, int) or idade <= 0:
        return jsonify({'message': 'Erro: Idade deve ser um número inteiro positivo.'}), 400

    cursor = conn.cursor()
    cursor.execute('UPDATE users SET nome = %s, email = %s, idade = %s WHERE id = %s', (nome, email, idade, user_id))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Usuário atualizado com sucesso.'}), 200

@app.route('/api/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the user to delete
    responses:
      200:
        description: User deleted successfully
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Usuário excluído com sucesso.'}), 200

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    """
    List all orders
    ---
    responses:
      200:
        description: A list of orders
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    cursor.close()
    return jsonify(pedidos)

@app.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    """
    Get order by ID
    ---
    parameters:
      - name: pedido_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the order to get
    responses:
      200:
        description: Details of the order
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos WHERE id = %s', (pedido_id,))
    pedido = cursor.fetchone()
    cursor.close()
    if pedido:
        return jsonify(pedido)
    else:
        return jsonify({'message': 'Pedido não encontrado.'}), 404

@app.route('/api/pedidos/add', methods=['POST'])
def add_pedido():
    """
    Add a new order
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Pedido
          required:
            - usuario_id
            - descricao
            - produtos
          properties:
            usuario_id:
              type: integer
              description: ID of the user associated with the order
            descricao:
              type: string
              description: Description of the order
            produtos:
              type: array
              items:
                type: integer
              description: List of product IDs associated with the order
    responses:
      201:
        description: Order added successfully
    """
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    descricao = data.get('descricao')
    produtos = data.get('produtos')
    status = data.get('status')

    if usuario_id is None or descricao is None or produtos is None:
        return jsonify({'message': 'Erro: Todos os campos (usuario_id, descricao, produtos) são obrigatórios.'}), 400
    
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pedidos (usuario_id, descricao, status) VALUES (%s, %s, %s) RETURNING id', (usuario_id, descricao, status))
    pedido_id = cursor.fetchone()[0]

    for produto_id in produtos:
        cursor.execute('INSERT INTO pedidos_produtos (pedido_id, produto_id) VALUES (%s, %s)', (pedido_id, produto_id))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Pedido adicionado com sucesso.'}), 201

@app.route('/api/pedidos/update/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    """
    Update order by ID
    ---
    parameters:
      - name: pedido_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the order to update
      - name: body
        in: body
        required: true
        schema:
          id: PedidoUpdate
          properties:
            usuario_id:
              type: integer
              description: Updated ID of the user associated with the order
            descricao:
              type: string
              description: Updated description of the order
            produtos:
              type: array
              items:
                type: integer
              description: Updated list of product IDs associated with the order
            status:
              type: string
              description: Updated status of the order
    responses:
      200:
        description: Order updated successfully
    """
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    descricao = data.get('descricao')
    produtos = data.get('produtos')
    status = data.get('status')

    if usuario_id is None or descricao is None or produtos is None:
        return jsonify({'message': 'Erro: Todos os campos (usuario_id, descricao, produtos) são obrigatórios.'}), 400

    cursor = conn.cursor()
    cursor.execute('UPDATE pedidos SET usuario_id = %s, descricao = %s, status = %s WHERE id = %s', (usuario_id, descricao, status, pedido_id))
    
    cursor.execute('DELETE FROM pedidos_produtos WHERE pedido_id = %s', (pedido_id,))
    for produto_id in produtos:
        cursor.execute('INSERT INTO pedidos_produtos (pedido_id, produto_id) VALUES (%s, %s)', (pedido_id, produto_id))

    conn.commit()
    cursor.close()

    return jsonify({'message': 'Pedido atualizado com sucesso.'}), 200

@app.route('/api/pedidos/delete/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    """
    Delete order by ID
    ---
    parameters:
      - name: pedido_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the order to delete
    responses:
      200:
        description: Order deleted successfully
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pedidos_produtos WHERE pedido_id = %s', (pedido_id,))
    cursor.execute('DELETE FROM pedidos WHERE id = %s', (pedido_id,))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Pedido excluído com sucesso.'}), 200

@app.route('/api/pedidos_produtos', methods=['GET'])
def get_pedidos_produtos():
    """
    List all orders associated with products
    ---
    responses:
      200:
        description: A list of orders associated with products
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos_produtos')
    pedidos_produtos = cursor.fetchall()
    cursor.close()
    response = []
    for pedido_produto in pedidos_produtos:
        pedido_id, produto_id = pedido_produto
        response.append({'pedido_id': pedido_id, 'produto_id': produto_id})

    return jsonify(response)

@app.route('/api/pedidos_produtos/add', methods=['POST'])
def add_pedido_produto():
    """
    Add a product to an order
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: PedidoProduto
          required:
            - pedido_id
            - produto_id
          properties:
            pedido_id:
              type: integer
              description: ID of the order to associate the product with
            produto_id:
              type: integer
              description: ID of the product to be associated with the order
    responses:
      201:
        description: Product added to order successfully
    """
    data = request.get_json()
    pedido_id = data.get('pedido_id')
    produto_id = data.get('produto_id')

    if pedido_id is None or produto_id is None:
        return jsonify({'message': 'Erro: Os campos pedido_id e produto_id são obrigatórios.'}), 400

    cursor = conn.cursor()
    cursor.execute('INSERT INTO pedidos_produtos (pedido_id, produto_id) VALUES (%s, %s)', (pedido_id, produto_id))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Produto associado ao pedido com sucesso.'}), 201

@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    """
    List all products
    ---
    responses:
      200:
        description: A list of products
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    cursor.close()
    produtos = [{'id': p[0], 'nome': p[1], 'preco': float(p[2])} for p in produtos]
    return jsonify(produtos)

@app.route('/api/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    """
    Get product by ID
    ---
    parameters:
      - name: produto_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the product to get
    responses:
      200:
        description: Details of the product
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = %s', (produto_id,))
    produto = cursor.fetchone()
    cursor.close()
    if produto:
        return jsonify(produto)
    else:
        return jsonify({'message': 'Produto não encontrado.'}), 404

@app.route('/api/produtos/add', methods=['POST'])
def add_produto():
    """
    Add a new product
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Produto
          required:
            - nome
            - preco
          properties:
            nome:
              type: string
              description: Name of the product
            preco:
              type: number
              description: Price of the product
    responses:
      201:
        description: Product added successfully
    """
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')

    # Validar os dados recebidos
    if nome is None or preco is None:
        return jsonify({'message': 'Erro: Todos os campos (nome, preco) são obrigatórios.'}), 400

    if not isinstance(preco, (int, float)) or preco <= 0:
        return jsonify({'message': 'Erro: Preço deve ser um número positivo.'}), 400
    
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (nome, preco) VALUES (%s, %s)', (nome, preco))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Produto adicionado com sucesso.'}), 201

@app.route('/api/produtos/update/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    """
    Update product by ID
    ---
    parameters:
      - name: produto_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the product to update
      - name: body
        in: body
        required: true
        schema:
          id: ProdutoUpdate
          properties:
            nome:
              type: string
              description: Updated name of the product
            preco:
              type: number
              description: Updated price of the product
    responses:
      200:
        description: Product updated successfully
    """
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')

    if nome is None or preco is None:
        return jsonify({'message': 'Erro: Todos os campos (nome, preco) são obrigatórios.'}), 400

    cursor = conn.cursor()
    cursor.execute('UPDATE produtos SET nome = %s, preco = %s WHERE id = %s', (nome, preco, produto_id))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Produto atualizado com sucesso.'}), 200

@app.route('/api/produtos/delete/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    """
    Delete product by ID
    ---
    parameters:
      - name: produto_id
        in: path
        type: integer
        required: true
        description: Numeric ID of the product to delete
    responses:
      200:
        description: Product deleted successfully
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = %s', (produto_id,))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Produto excluído com sucesso.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
