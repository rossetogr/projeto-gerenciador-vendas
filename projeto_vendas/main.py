import sys
import os

# Ajusta o PYTHONPATH para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from database.models import init_db
from services.produtos import cadastrar_produto, listar_produtos, editar_produto, remover_produto
from services.vendas import registrar_venda
from services.relatorios import (
    relatorio_total_vendido, 
    relatorio_produto_mais_vendido, 
    relatorio_lucro_estimado
)

def menu_principal():
    """Exibe o menu principal do sistema."""
    print("\n" + "="*40)
    print("  SISTEMA DE CONTROLE DE VENDAS (CLI)")
    print("="*40)
    print(" [1] Gerenciar Produtos")
    print(" [2] Registrar Venda")
    print(" [3] Gerar Relatórios")
    print(" [0] Sair")
    print("-" * 40)
    return input("Escolha uma opção: ")

def menu_produtos():
    """Exibe o menu de gerenciamento de produtos."""
    print("\n--- Gerenciar Produtos ---")
    print(" [1] Cadastrar Novo Produto")
    print(" [2] Listar Produtos (Ver Estoque)")
    print(" [3] Editar Produto")
    print(" [4] Remover Produto")
    print(" [0] Voltar ao Menu Principal")
    print("-" * 30)
    return input("Escolha uma opção: ")

def menu_relatorios():
    """Exibe o menu de relatórios."""
    print("\n--- Gerar Relatórios ---")
    print(" [1] Total Vendido HOJE")
    print(" [2] Total Vendido no MÊS")
    print(" [3] Produto Mais Vendido (Unidades)")
    print(" [4] Lucro Estimado HOJE")
    print(" [5] Lucro Estimado no MÊS")
    print(" [0] Voltar ao Menu Principal")
    print("-" * 35)
    return input("Escolha uma opção: ")

def main():
    """Função principal do sistema."""
    # 1. Inicializa o Banco de Dados
    init_db()

    while True:
        opcao_principal = menu_principal()

        match opcao_principal:
            case '1':
                while True:
                    match menu_produtos():
                        case '1':
                            cadastrar_produto()
                        case '2':
                            listar_produtos()
                        case '3':
                            editar_produto()
                        case '4':
                            remover_produto()
                        case '0':
                            break
                        case _:
                            print("Opção inválida. Tente novamente.")
        
            case '2':
                registrar_venda()

            case '3':
                while True:
                    match menu_relatorios():
                        case '1':
                            relatorio_total_vendido('dia')
                        case '2':
                            relatorio_total_vendido('mes')
                        case '3':
                            relatorio_produto_mais_vendido()
                        case '4':
                            relatorio_lucro_estimado('dia')
                        case '5':
                            relatorio_lucro_estimado('mes')
                        case '0':
                            break
                        case _:
                            print("Opção inválida. Tente novamente.")

            case '0':
                print("\nObrigado por usar o Sistema de Controle de Vendas. Até mais!")
                break
            
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()