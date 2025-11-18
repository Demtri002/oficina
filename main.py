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
    confirm = input("Isso irá APAGAR TODOS os dados. Deseja recriar o banco? (s/n): ")
    if confirm.lower() == 's':
        eliminar_tabelas(conn)
        criar_tabelas(conn)
        print("--- Banco de dados recriado ---")
    else:
        print("Operação cancelada.")

def menu_cadastros(conn):
    while True:
        print("\n--- Menu de Cadastros ---")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Veículo")
        print("3. Cadastrar Agendamento")
        print("4. Cadastrar Mecânico")        
        print("5. Cadastrar tipos de Serviço")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            print("--- Novo Cliente ---")
            nome = input("Nome: ")
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            if nome and cpf:
                cadastrar_cliente(conn, nome, cpf, endereco, telefone)
            else:
                print("Nome e CPF são obrigatórios.")
        
        elif escolha == '2':
            print("--- Novo Veículo ---")
            cpf_cliente = input("Digite o CPF do cliente dono do veículo: ")
            cliente = buscar_cliente_por_cpf(conn, cpf_cliente)
            
            if cliente:
                id_cliente, nome_cliente = cliente
                print(f"Cliente encontrado: {nome_cliente}")
                placa = input("Placa (7 dígitos): ").upper()
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                if placa and id_cliente and marca and modelo:
                    cadastrar_veiculo(conn, placa, id_cliente, marca, modelo)
                else:
                    print("Placa, Marca e Modelo são obrigatórios.")
            else:
                print("Cliente não encontrado. Cadastre o cliente primeiro.")
        
        elif escolha == '3':
            print("--- Novo Agendamento ---")
            placa = input("Placa do veículo: ").upper()
            if not buscar_veiculo_por_placa(conn, placa):
                print("Veículo não cadastrado. Cadastre o veículo primeiro.")
                continue # Volta ao menu de cadastros
            
            servicos = listar_servicos_simples(conn)
            if not servicos:
                print("Cadastre os tipos de serviço primeiro.")
                continue
                
            id_servico = input("Digite o ID do serviço desejado: ")
            data = input("Data e Hora (Formato: AAAA-MM-DD HH:MM): ")
            
            cadastrar_agendamento(conn, placa, int(id_servico), data)
            
        elif escolha == '4':
            print("--- Novo Mecânico ---")
            nome = input("Nome: ")
            cargo = input("Cargo (Ex: Chefe de Oficina, Eletricista): ")
            if nome and cargo:
                cadastrar_mecanico(conn, nome, cargo)
            else:
                print("Nome e Cargo são obrigatórios.")

        elif escolha == '5':
            print("--- Novo Tipo de Serviço ---") 
            nome = input("Nome do Serviço (Ex: Troca de Óleo): ") 
            preco = input("Preço Padrão (Ex: 150.00): ")
            
            if nome and preco:
                try:
                    preco_float = float(preco)
                    cadastrar_tipo_servico(conn, nome, preco_float)
                except ValueError:
                    print("Erro: O preço deve ser um número (ex: 150.00)")
            else:
                print("Nome e Preço são obrigatórios.")

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
        print("4. Consultar Serviços Realizados")
        print("5. Consultar Faturamento Mensal")
        print("6. Consultar com Gemini")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            listar_clientes(conn)
        elif escolha == '2':
            listar_veiculos(conn)
        elif escolha == '3':
            listar_agendamentos(conn)
        elif escolha == '4':
            listar_servicos_realizados(conn)
        elif escolha == '5':
            consultar_faturamento_mensal(conn)
        elif escolha == '6':
            prompt = input("Faça sua pergunta: ")
            perguntar_ao_banco_com_ia(prompt, conn)
        elif escolha == '0':
            break
        else:
            print("Escolha inválida.")

def menu_atualizacoes(conn):
    while True:
        print("\n--- Menu de Atualizações ---")
        print("1. Atualizar Cadastro de Cliente")
        print("2. Atualizar Cadastro de Mecânico")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            print("--- Atualizar Cliente ---")
            listar_clientes(conn) 
            try:
                id_cli = int(input("Digite o ID do cliente que deseja alterar: "))
                nome = input(f"Novo Nome (ID {id_cli}): ")
                cpf = input(f"Novo CPF (ID {id_cli}): ")
                endereco = input(f"Novo Endereço (ID {id_cli}): ")
                telefone = input(f"Novo Telefone (ID {id_cli}): ")
                
                if id_cli and nome and cpf:
                    atualizar_cliente(conn, id_cli, nome, cpf, endereco, telefone)
                else:
                    print("ID, Nome e CPF são obrigatórios.")
            except ValueError:
                print("ID inválido.")
                
        elif escolha == '2':
            print("--- Atualizar Mecânico ---")
            try:
                id_mec = int(input("Digite o ID do mecânico que deseja alterar: "))
                nome = input(f"Novo Nome (ID {id_mec}): ")
                cargo = input(f"Novo Cargo (ID {id_mec}): ")
                
                if id_mec and nome and cargo:
                    atualizar_mecanico(conn, id_mec, nome, cargo)
                else:
                    print("ID, Nome e Cargo são obrigatórios.")
            except ValueError:
                print("ID inválido.")
                
        elif escolha == '0':
            break
        else:
            print("Escolha inválida.")

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
                    print("2. Relatórios")
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
            print("Verifique se o PostgreSQL está rodando e se o banco 'oficina' existe.")
            
    except Exception as e:
        print(f"Ocorreu um erro crítico no programa: {e}")
    finally:
        if conn:
            encerra_conexao(conn)