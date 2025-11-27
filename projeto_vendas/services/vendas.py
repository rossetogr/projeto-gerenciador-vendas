from database.conexao import get_db_connection
from utils.validacao import get_int_input
from services.produtos import listar_produtos
from datetime import datetime

def registrar_venda():
    """
    Registra uma venda, verifica e atualiza o estoque.
    Impede a venda se o estoque for insuficiente.
    """
    listar_produtos()
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    # Verifica se há produtos para vender
    if not cursor.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]:
        print("\n🚫 Não há produtos cadastrados para realizar vendas.")
        conn.close()
        return

    try:
        produto_id = get_int_input("\nID do Produto vendido: ")
        
        # 1. Verificar o estoque atual do produto
        cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print(f"🚫 Produto com ID {produto_id} não encontrado.")
            conn.close()
            return
        
        estoque_atual = produto['quantidade']
        print(f"Estoque atual de '{produto['nome']}': {estoque_atual} unidades.")

        quantidade_vendida = get_int_input("Quantidade vendida: ", min_value=1)

        # 2. Impedir venda sem estoque
        if quantidade_vendida > estoque_atual:
            print(f"\n❌ Venda impedida! Estoque insuficiente ({estoque_atual} restantes).")
            conn.close()
            return

        # 3. Registrar a venda
        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade, data)
            VALUES (?, ?, ?)
        """, (produto_id, quantidade_vendida, data_venda))
        
        # 4. Atualizar o estoque
        novo_estoque = estoque_atual - quantidade_vendida
        cursor.execute("""
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
        """, (novo_estoque, produto_id))

        conn.commit()
        print(f"\n✅ Venda registrada com sucesso!")
        print(f"   - Produto: {produto['nome']}")
        print(f"   - Quantidade: {quantidade_vendida}")
        print(f"   - Novo Estoque: {novo_estoque}")

    except Exception as e:
        print(f"\n❌ Erro ao registrar venda: {e}")
        # Se ocorrer um erro no meio, o rollback garante que nenhuma parte da transação
        # (registro de venda ou atualização de estoque) seja salva.
        conn.rollback() 
    finally:
        conn.close()