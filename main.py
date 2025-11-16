# Importa as funções necessárias do módulo de banco de dados
from database import (
    conecta, 
    encerra_conexao, 
    eliminar_tabelas, 
    criar_tabelas, 
    cadastrar_cliente
)

def executar_setup_inicial(conn):
    """Executa a limpeza (DROP) e a criação (CREATE) das tabelas."""
    print("--- Iniciando Setup Automático ---")
    
    print("Limpando banco de dados (DROP CASCADE)...")
    eliminar_tabelas(conn)
    
    print("Criando nova estrutura de tabelas...")
    criar_tabelas(conn)
    
    print("--- Setup Concluído ---")

def menu_principal(conn):
    """Exibe o menu de operações após o setup."""
    
    while True:
        print("\n--- Menu Principal da Oficina ---")
        print("1. Cadastrar Cliente")
        print("2. Sair")
        
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            try:
                nome = input("Digite o nome do cliente: ")
                email = input("Digite o email do cliente: ")
                senha = input("Digite a senha do cliente: ")
                
                if not nome or not email: 
                    print("Erro: Nome e Email são obrigatórios.")
                    continue 

                cadastrar_cliente(conn, nome, email, senha)
                
            except Exception as e:
                print(f"Erro durante o cadastro: {e}")

        elif escolha == '2':
            print("Saindo...")
            break 
            
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    conn = None 
    try:
        conn = conecta()
        
        if conn:
            executar_setup_inicial(conn)
            
            menu_principal(conn)
            
    except Exception as e:
        print(f"Ocorreu um erro crítico no programa: {e}")
    finally:
        if conn:
            encerra_conexao(conn)