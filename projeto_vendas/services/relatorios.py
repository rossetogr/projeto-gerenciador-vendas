from database.conexao import get_db_connection
from datetime import datetime

def formatar_moeda(valor):
    """Formata o valor para o padrão de moeda brasileira."""
    return f"R$ {valor:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')

def relatorio_total_vendido(periodo='dia'):
    """
    Calcula o total vendido (monetário) em um determinado período ('dia' ou 'mês').
    Usa JOIN para acessar o preço do produto.
    """
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    data_atual = datetime.now()
    filtro_data = ""
    titulo = ""

    if periodo == 'dia':
        data_string = data_atual.strftime("%Y-%m-%d")
        filtro_data = f"WHERE STRFTIME('%Y-%m-%d', v.data) = '{data_string}'"
        titulo = f"Total Vendido no Dia ({data_string})"
    elif periodo == 'mes':
        mes_ano_string = data_atual.strftime("%Y-%m")
        filtro_data = f"WHERE STRFTIME('%Y-%m', v.data) = '{mes_ano_string}'"
        titulo = f"Total Vendido no Mês ({mes_ano_string})"
    else:
        print("Período inválido para relatório.")
        conn.close()
        return

    try:
        # Consulta com JOIN e SUM:
        # p.preco * v.quantidade = Valor total da venda
        cursor.execute(f"""
            SELECT SUM(p.preco * v.quantidade) AS total_vendido
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            {filtro_data};
        """)
        
        resultado = cursor.fetchone()['total_vendido']
        total = resultado if resultado is not None else 0.0

        print(f"\n--- {titulo} ---")
        print(f"Valor Total: {formatar_moeda(total)}")
        print("-" * (len(titulo) + 12))

    except Exception as e:
        print(f"\n❌ Erro ao gerar relatório de vendas: {e}")
    finally:
        conn.close()

def relatorio_produto_mais_vendido():
    """
    Identifica o produto mais vendido em termos de unidades.
    Usa GROUP BY e SUM.
    """
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    try:
        # Consulta com GROUP BY e SUM:
        # Soma a quantidade vendida por produto e ordena
        cursor.execute("""
            SELECT 
                p.nome, 
                SUM(v.quantidade) AS total_unidades_vendidas
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            GROUP BY p.nome
            ORDER BY total_unidades_vendidas DESC
            LIMIT 5; -- Mostra os 5 mais vendidos
        """)
        
        produtos = cursor.fetchall()

        print("\n--- Top 5 Produtos Mais Vendidos (em Unidades) ---")
        if not produtos:
            print("Nenhuma venda registrada ainda.")
            return

        print("{:<30} | {:<10}".format("Produto", "Unidades"))
        print("-" * 43)
        for prod in produtos:
            print("{:<30} | {:<10}".format(prod['nome'], prod['total_unidades_vendidas']))
        print("-" * 43)

    except Exception as e:
        print(f"\n❌ Erro ao gerar relatório de produto mais vendido: {e}")
    finally:
        conn.close()

def relatorio_lucro_estimado(periodo='mes'):
    """
    Calcula o lucro estimado em um determinado período ('dia' ou 'mês').
    Lucro = (Preço de Venda - Custo) * Quantidade Vendida.
    """
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    data_atual = datetime.now()
    filtro_data = ""
    titulo = ""

    if periodo == 'dia':
        data_string = data_atual.strftime("%Y-%m-%d")
        filtro_data = f"WHERE STRFTIME('%Y-%m-%d', v.data) = '{data_string}'"
        titulo = f"Lucro Estimado no Dia ({data_string})"
    elif periodo == 'mes':
        mes_ano_string = data_atual.strftime("%Y-%m")
        filtro_data = f"WHERE STRFTIME('%Y-%m', v.data) = '{mes_ano_string}'"
        titulo = f"Lucro Estimado no Mês ({mes_ano_string})"
    else:
        print("Período inválido para relatório.")
        conn.close()
        return

    try:
        # Consulta com JOIN e SUM:
        # (p.preco - p.custo) * v.quantidade = Lucro da transação
        cursor.execute(f"""
            SELECT SUM((p.preco - p.custo) * v.quantidade) AS lucro_total
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            {filtro_data};
        """)
        
        resultado = cursor.fetchone()['lucro_total']
        lucro = resultado if resultado is not None else 0.0

        print(f"\n--- {titulo} ---")
        print(f"Lucro Estimado: {formatar_moeda(lucro)}")
        print("-" * (len(titulo) + 16))

    except Exception as e:
        print(f"\n❌ Erro ao gerar relatório de lucro: {e}")
    finally:
        conn.close()