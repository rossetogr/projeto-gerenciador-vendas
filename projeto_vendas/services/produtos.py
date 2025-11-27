from database.conexao import get_db_connection
from utils.validacao import get_float_input, get_int_input

def cadastrar_produto():
    """Cadastra um novo produto no banco de dados."""
    nome = input("Nome do Produto: ").strip()
    if not nome:
        print("O nome do produto não pode ser vazio.")
        return

    # Usando a função de validação para garantir inputs corretos
    preco = get_float_input("Preço de Venda (Ex: 19.99): R$ ")
    custo = get_float_input("Custo de Aquisição (para cálculo de lucro): R$ ")
    quantidade = get_int_input("Quantidade Inicial em Estoque: ")

    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO produtos (nome, preco, custo, quantidade)
            VALUES (?, ?, ?, ?)
        """, (nome, preco, custo, quantidade))
        conn.commit()
        print(f"\n✅ Produto '{nome}' cadastrado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao cadastrar produto (Nome já existe?): {e}")
    finally:
        conn.close()

def listar_produtos():
    """Lista todos os produtos no estoque."""
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nome, preco, custo, quantidade FROM produtos ORDER BY nome")
        produtos = cursor.fetchall()

        if not produtos:
            print("\nNenhum produto cadastrado.")
            return

        print("\n--- Lista de Produtos em Estoque ---")
        print("{:<4} | {:<30} | {:<10} | {:<10} | {:<10}".format("ID", "Nome", "Preço", "Custo", "Estoque"))
        print("-" * 68)
        for p in produtos:
            print("{:<4} | {:<30} | R$ {:<7.2f} | R$ {:<7.2f} | {:<10}".format(
                p['id'], p['nome'], p['preco'], p['custo'], p['quantidade']))
        print("-" * 68)

    except Exception as e:
        print(f"\n❌ Erro ao listar produtos: {e}")
    finally:
        conn.close()

def editar_produto():
    """Edita um produto existente pelo ID."""
    listar_produtos()
    if not get_db_connection().cursor().execute("SELECT COUNT(*) FROM produtos").fetchone()[0]:
        return

    produto_id = get_int_input("\nID do Produto para editar: ")
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    # 1. Verificar se o produto existe
    cursor.execute("SELECT nome, preco, custo, quantidade FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        print(f"Produto com ID {produto_id} não encontrado.")
        conn.close()
        return

    print(f"\n-- Editando Produto: {produto['nome']} --")
    print("Deixe em branco para manter o valor atual.")

    # Obter novos valores, mantendo os antigos como default
    novo_nome = input(f"Novo Nome (Atual: {produto['nome']}): ").strip() or produto['nome']
    
    while True:
        preco_str = input(f"Novo Preço de Venda (Atual: R$ {produto['preco']:.2f}): R$ ").replace(',', '.')
        if not preco_str:
            novo_preco = produto['preco']
            break
        try:
            novo_preco = float(preco_str)
            if novo_preco < 0:
                 print("O preço não pode ser negativo.")
                 continue
            break
        except ValueError:
            print("Entrada inválida. Digite um número ou deixe em branco.")

    while True:
        custo_str = input(f"Novo Custo de Aquisição (Atual: R$ {produto['custo']:.2f}): R$ ").replace(',', '.')
        if not custo_str:
            novo_custo = produto['custo']
            break
        try:
            novo_custo = float(custo_str)
            if novo_custo < 0:
                 print("O custo não pode ser negativo.")
                 continue
            break
        except ValueError:
            print("Entrada inválida. Digite um número ou deixe em branco.")

    while True:
        qtd_str = input(f"Nova Quantidade em Estoque (Atual: {produto['quantidade']}): ")
        if not qtd_str:
            nova_quantidade = produto['quantidade']
            break
        try:
            nova_quantidade = int(qtd_str)
            if nova_quantidade < 0:
                 print("A quantidade não pode ser negativa.")
                 continue
            break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro ou deixe em branco.")

    try:
        cursor.execute("""
            UPDATE produtos 
            SET nome = ?, preco = ?, custo = ?, quantidade = ?
            WHERE id = ?
        """, (novo_nome, novo_preco, novo_custo, nova_quantidade, produto_id))
        conn.commit()
        print(f"\n✅ Produto ID {produto_id} ('{novo_nome}') atualizado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao atualizar produto: {e}")
    finally:
        conn.close()

def remover_produto():
    """Remove um produto existente pelo ID."""
    listar_produtos()
    if not get_db_connection().cursor().execute("SELECT COUNT(*) FROM produtos").fetchone()[0]:
        return

    produto_id = get_int_input("\nID do Produto para remover: ")
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    try:
        # Verifica se há vendas associadas (boa prática, mas o ON DELETE CASCADE é mais robusto)
        # Vamos apenas deletar, pois o banco de dados está isolado.
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        if cursor.rowcount == 0:
            print(f"Produto com ID {produto_id} não encontrado.")
        else:
            conn.commit()
            print(f"✅ Produto ID {produto_id} removido com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao remover produto: {e}")
    finally:
        conn.close()