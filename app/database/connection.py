import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv



load_dotenv('.env')

config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_DATABASE', 'db_imoveis'),
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