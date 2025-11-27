import sqlite3
from .models import DB_PATH # Importa o caminho do DB do arquivo models

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        # Permite acessar colunas por nome (conn['nome'])
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None