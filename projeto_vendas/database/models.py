import sqlite3
import os

# Nome do arquivo do banco de dados
DB_NAME = 'vendas_local.db'
# Caminho para o diretório do banco de dados (dentro da pasta 'database')
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def init_db():
    """
    Inicializa o banco de dados e cria as tabelas 'produtos' e 'vendas'.
    A coluna 'custo' é adicionada em 'produtos' para cálculo de lucro.
    """
    conn = None
    try:
        # Tenta conectar ao DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Tabela PRODUTOS
        # preco: Preço de Venda
        # custo: Custo de Aquisição (necessário para calcular o lucro)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                preco REAL NOT NULL,
                custo REAL NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0
            );
        """)

        # Tabela VENDAS
        # produto_id: FOREIGN KEY para a tabela produtos
        # data: Armazena a data da venda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            );
        """)

        # Índice em produto_id na tabela vendas para consultas rápidas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendas_produto_id ON vendas (produto_id);")

        conn.commit()
        print(f"Banco de dados '{DB_NAME}' inicializado com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Executa a inicialização do DB se o script for rodado diretamente
    init_db()