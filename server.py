from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Permite que o frontend se comunique com o backend

# Função para conectar ao banco de dados SQL Server
def conectar_bd():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=seu_servidor;'  # Substitua pelo nome ou IP do seu servidor
        'DATABASE=seu_banco_de_dados;'  # Substitua pelo nome do seu banco de dados
        'UID=seu_usuario;'  # Substitua pelo seu usuário
        'PWD=sua_senha;'  # Substitua pela sua senha
    )
    return conn

# Rota para salvar os dados no banco
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json  # Recebe os dados do frontend

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Inserir dados na tabela de vendedores (se não existir)
        cursor.execute("""
            INSERT INTO vendedores (nome_vendedor, telefone_vendedor)
            VALUES (?, ?)
        """, (data['nome_vendedor'], data['telefone_vendedor']))
        
        # Obter o ID do vendedor inserido
        cursor.execute("SELECT @@IDENTITY AS id")
        vendedor_id = cursor.fetchone()[0]
        
        # Inserir dados na tabela de clientes
        cursor.execute("""
            INSERT INTO clientes (razao_social, nome_fantasia, cidade, endereco, numero_rua, bairro, cep, cnpj, email, numero_contrato_social, telefone, codvendedores)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['razao_social'], data['nome_fantasia'], data['cidade'], data['endereco'], data['numero_rua'],
            data['bairro'], data['cep'], data['cnpj'], data['email'], data['numero_contrato_social'],
            data['telefone'], vendedor_id  # A chave estrangeira codvendedores será preenchida com o id do vendedor
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Pedido cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Função para gerar o PDF (sem alteração)
@app.route('/gerar_pdf', methods=['GET'])
def gerar_pdf():
    # Implementação da geração do PDF
    return jsonify({"message": "Gerando PDF..."}), 200

# Iniciar servidor Flask
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
