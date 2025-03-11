from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Permite que o frontend se comunique com o backend

# Conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect("clientes.db")

# Criar tabela no banco de dados
def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razao_social TEXT,
            nome_fantasia TEXT,
            cidade TEXT,
            endereco TEXT,
            numero_rua TEXT,
            bairro TEXT,
            cep TEXT,
            cnpj TEXT,
            email TEXT,
            numero_contrato_social TEXT,
            telefone TEXT,
            nome_vendedor TEXT,
            telefone_vendedor TEXT
        )
    """)
    conn.commit()
    conn.close()

# Rota para a página principal
@app.route('/')
def home():
    return "Bem-vindo ao sistema de pedidos!"

# Rota para salvar os dados no banco
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json  # Recebe os dados do frontend

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedidos (razao_social, nome_fantasia, cidade, endereco, numero_rua, bairro, cep, cnpj, email, numero_contrato_social, telefone, nome_vendedor, telefone_vendedor) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['razao_social'], data['nome_fantasia'], data['cidade'], data['endereco'], data['numero_rua'],
            data['bairro'], data['cep'], data['cnpj'], data['email'], data['numero_contrato_social'], 
            data['telefone'], data['nome_vendedor'], data['telefone_vendedor']
        ))
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Pedido cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar servidor Flask
if __name__ == '__main__':
    criar_tabela()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
