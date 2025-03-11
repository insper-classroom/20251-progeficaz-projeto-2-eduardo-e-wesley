from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.cred')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}


# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


app = Flask(__name__)


@app.route('/alunos', methods=['GET'])
def get_alunos():

    # conectar colm a base
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()

    sql = "SELECT * from tbl_alunos"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum aluno encontrado"}
        return resp, 404
    else:
        alunos = []
        for aluno in results:
            aluno_dict = {
                "id": aluno[0],
                "nome": aluno[1],
                "frase": aluno[2]
            }
            alunos.append(aluno_dict)

        resp = {"alunos": alunos}
        return resp, 200


@app.route('/delete', methods=["DELETE"])
def delete_conteudo():
    conn = connect_db()
    
    if conn is None:
        return {'Erro': "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_alunos WHERE id=3")
    rows_deleted = cursor.rowcount  # Obtém o número de linhas deletadas
    conn.commit()  # Confirma a exclusão

    if rows_deleted > 0:
        resposta = {"Mensagem": f'Foram apagados {rows_deleted} items'}
        status_code = 200
    else:
        resposta = {'Erro': "Nenhum aluno encontrado com o ID fornecido"}
        status_code = 404

    cursor.close()
    conn.close()
    
    return resposta, status_code


@app.route('/atualiza', methods=['PATCH'])
def atualiza_conteudo():
    conn = connect_db()
    if conn is None:
        return {'Erro':'Erro ao conectar com o banco de dados'}, 500

    cursor = conn.cursor()
    cursor.execute('')



if __name__ == '__main__':
    app.run(debug=True)