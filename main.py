from database import *
from ai_integration import perguntar_ao_banco_com_ia

def login_mecanico():
    print("--- Sistema de Gerenciamento da Oficina ---")
    nome = input("Digite seu nome (Mecânico/Admin) para logar: ")
    if not nome:
        print("Login inválido.")
        return False
        
    print(f"Bem-vindo, {nome}!")
    return True

def executar_setup_inicial(conn):
    print("--- ATENÇÃO: MODO ADMIN ---")
    print("Esta operação apagará TODAS as tabelas e dados existentes.")
    confirm = input("Tem certeza que deseja zerar o banco? (s/n): ")
    if confirm.lower() == 's':
        eliminar_tabelas(conn)
        criar_tabelas(conn)
        print("--- Banco de dados recriado com sucesso! ---")
    else:
        print("Operação cancelada.")

def menu_cadastros(conn):
    while True:
        print("\n--- Menu de Cadastros ---")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Veículo")
        print("3. Cadastrar Agendamento")
        print("4. Cadastrar Mecânico")        
        print("5. Cadastrar Tipos de Serviço")
        print("6. Cadastrar Peça")
        print("7. Cadastrar Fornecedor")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            print("\n--- Novo Cliente ---")
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")
            
            if nome:
                cadastrar_cliente(conn, nome, telefone, email, cpf, endereco)
            else:
                print("Nome é obrigatório.")
        
        elif escolha == '2':
            print("\n--- Novo Veículo ---")
    
            cpf_cliente = input("Digite o CPF do proprietário: ") # Agora pede o CPF
            placa = input("Placa (7 caracteres): ").upper()
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            cor = input("Cor: ")
    
            try:
                ano = int(input("Ano: "))
        
                if placa and marca and modelo and cpf_cliente:
                    cadastrar_veiculo(conn, marca, cor, ano, modelo, placa, cpf_cliente)
                else:
                    print("Todos os dados são obrigatórios.")
            except ValueError:
                print("Erro: O Ano deve ser numérico.")
        
        elif escolha == '3':
            print("\n--- Novo Agendamento ---")
            listar_veiculos(conn) 

            placa = input("Digite a Placa do Veículo: ").upper()
            data = input("Data e Hora (AAAA-MM-DD HH:MM:SS): ")
    
            if placa and data:
                cadastrar_agendamento(conn, data, placa)
            else:
                print("Placa e Data são obrigatórios.")
            
        elif escolha == '4':
            print("\n--- Novo Mecânico ---")
            nome = input("Nome: ")
            cargo = input("Cargo: ")
            email = input("Email: ")
            
            # Opcional: Supervisor
            tem_supervisor = input("Tem supervisor? (s/n): ").lower()
            id_supervisor = None
            if tem_supervisor == 's':
                id_supervisor = input("ID do Supervisor: ")
            
            if nome and cargo:
                cadastrar_mecanico(conn, nome, cargo, email, id_supervisor)
            else:
                print("Nome e Cargo são obrigatórios.")

        elif escolha == '5':
            print("\n--- Novo Tipo de Serviço ---") 
            nome = input("Nome do Serviço: ") 
            descricao = input("Descrição: ")
            
            if nome:
                cadastrar_tipo_servico(conn, nome, descricao)
            else:
                print("Nome é obrigatório.")

        elif escolha == '6':
             print("\n--- Nova Peça ---")
             nome_peca = input("Nome da Peça: ")
             descricao = input("Descrição: ")
             try:
                 id_fornecedor = int(input("ID do Fornecedor: "))
                 cadastrar_peca(conn, nome_peca, descricao, id_fornecedor)
             except ValueError:
                 print("ID do fornecedor inválido.")

        elif escolha == '7':
            print("\n--- Novo Fornecedor ---")
            nome = input("Nome do Fornecedor: ")
            if nome:
                cadastrar_fornecedor(conn, nome)

        elif escolha == '0':
            break 
        else:
            print("Escolha inválida.")
        
    
def menu_relatorios(conn):
    while True:
        print("\n--- Menu de Relatórios ---")
        print("1. Consultar Clientes")
        print("2. Consultar Veículos")
        print("3. Consultar Agendamentos")
        print("4. Consultar Serviços Realizados (Não implementado)")
        print("6. Consultar com IA (Gemini)")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            listar_clientes(conn)
        elif escolha == '2':
            listar_veiculos(conn)
        elif escolha == '3':
            listar_agendamentos(conn)
        elif escolha == '6':
            print("\n--- Assistente Virtual ---")
            print("Ex: 'Liste todos os clientes', 'Quantos veículos temos?', 'Mostre os agendamentos'")
            prompt = input("Faça sua pergunta ao banco: ")
            perguntar_ao_banco_com_ia(prompt, conn)
        elif escolha == '0':
            break
        else:
            print("Escolha inválida.")

def menu_atualizacoes(conn):
    print("\nFuncionalidade de atualização precisa ser ajustada para a nova estrutura.")
    print("Use o pgAdmin ou implemente as funções 'atualizar_*' no database.py primeiro.")
    input("Pressione Enter para voltar...")

if __name__ == "__main__":
    conn = None
    try:
        conn = conecta()
        if conn:
            criar_tabelas(conn) 
            
            if login_mecanico():
                while True:
                    print("\n--- MENU PRINCIPAL ---")
                    print("1. Cadastros")
                    print("2. Relatórios / Consultas")
                    print("3. Atualizar Cadastros")
                    print("------------------------")
                    print("9. [Admin] Reiniciar Banco de Dados (APAGA TUDO)")
                    print("0. Sair do Sistema")
                    
                    escolha_main = input("Escolha uma opção: ")

                    if escolha_main == '1':
                        menu_cadastros(conn)
                    elif escolha_main == '2':
                        menu_relatorios(conn)
                    elif escolha_main == '3':
                        menu_atualizacoes(conn)
                    elif escolha_main == '9':
                        executar_setup_inicial(conn)
                    elif escolha_main == '0':
                        print("Saindo do sistema...")
                        break 
                    else:
                        print("Opção inválida.")
        else:
            print("Não foi possível conectar ao banco de dados.")
            print("Verifique se o PostgreSQL está rodando e as credenciais no database.py.")
            
    except Exception as e:
        print(f"Ocorreu um erro crítico no programa: {e}")
    finally:
        if conn:
            encerra_conexao(conn)