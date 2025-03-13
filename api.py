from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv('.cred')


config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_IMOVEL', 'db_cidade'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'ssl_ca': os.getenv('SSL_CA_PATH')
}

def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Erro: {err}")
        return None


app = Flask(__name__)


@app.route('/imoveis', methods=['GET'])
def get_imoveis():

    # conectar colm a base
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()

    sql = "SELECT * from tbl_imoveis"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum imovel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "imovel": imovel[1],
                "endereço": imovel[2]
            }
            imoveis.append(imovel_dict)

        resp = {"imoveis": imoveis}
        return resp, 200


@app.route('/delete', methods=["DELETE"])
def delete_conteudo():
    conn = connect_db()
    
    if conn is None:
        return {'Erro': "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_imoveis WHERE id=3")
    rows_deleted = cursor.rowcount  # Obtém o número de linhas deletadas
    conn.commit()  # Confirma a exclusão

    if rows_deleted > 0:
        resposta = {"Mensagem": f'Foram apagados {rows_deleted} items'}
        status_code = 200
    else:
        resposta = {'Erro': "Nenhum imovel encontrado com o ID fornecido"}
        status_code = 404

    cursor.close()
    conn.close()
    
    return resposta, status_code


if __name__ == '__main__':
    app.run(debug=True)