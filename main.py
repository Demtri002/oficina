from database import conecta, encerra_conexao



def insert_clientes(cursor, conection, nome, email, senha):
    """Insere um novo cliente e retorna o ID."""
    cmd_insert = "INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_cliente;" 
    values = nome, email, senha
    
    try:
        cursor.execute(cmd_insert, values)
        id_cliente = cursor.fetchone()[0]
        conection.commit()
        print(f'\n✅ Cadastro realizado com sucesso! ID: {id_cliente}')
        return id_cliente
    except Exception as e:
        conection.rollback()
        print(f"\n❌ Erro ao cadastrar cliente. Tente novamente. Detalhe: {e}")
        return None

def insert_veiculo(cursor, conection, id_veiculo, id_cliente, marca, modelo, cor, ano):
    """Insere um novo veículo associado a um cliente."""
    cmd_insert = "INSERT INTO veiculo (id_veiculo, id_cliente, marca, modelo, cor, ano) VALUES (%s, %s, %s, %s, %s, %s);"
    values = id_veiculo, id_cliente, marca, modelo, cor, ano
    
    try:
        cursor.execute(cmd_insert, values)
        conection.commit()
        print(f'✅ Veículo (Placa: {id_veiculo}) inserido com sucesso.')
    except Exception as e:
        conection.rollback()
        print(f"❌ Erro ao inserir veículo. Detalhe: {e}")

def insert_agendamento(cursor, conection, id_cliente, id_veiculo, data_agendamento):
    """Cria um novo agendamento."""
    cmd_insert = "INSERT INTO agendamento (id_cliente, id_veiculo, data_hora_agendada) VALUES (%s, %s, %s);"
    values = id_cliente, id_veiculo, data_agendamento
    
    try:
        cursor.execute(cmd_insert, values)
        conection.commit()
        print(f'✅ Agendamento marcado para {data_agendamento}.')
    except Exception as e:
        conection.rollback()
        print(f"❌ Erro ao agendar. Detalhe: {e}")

def fazer_login(cursor, email, senha):
    """Verifica as credenciais do usuário."""
    cmd_select = "SELECT id_cliente, senha FROM clientes WHERE email = %s;"
    cursor.execute(cmd_select, (email,))
    
    resultado = cursor.fetchone()
    
    if resultado:
        id_cliente, senha_armazenada = resultado
        if senha_armazenada == senha:
            return id_cliente
        else:
            print("\n❌ Senha incorreta.")
            return None
    else:
        print("\n❌ E-mail não encontrado.")
        return None



def fluxo_cadastro(cursor, conection):
    """Gerencia a coleta de dados para cadastro."""
    print("\n--- NOVO CADASTRO ---")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input ("Senha: ")
    insert_clientes(cursor, conection, nome, email, senha)

def fluxo_insercao_operacoes(cursor, conection, id_cliente):
    """Gerencia a inserção de veículo e agendamento após o login."""
    
    print(f"\n--- INSERÇÃO DE VEÍCULO (ID do Cliente: {id_cliente}) ---")
    
    placa = input("Insira a PLACA (ID do Veículo - 7 caracteres): ").upper()
    marca = input("Insira a marca: ")
    modelo = input("Insira o modelo: ")
    cor = input("Insira a cor: ")
    ano = input("Insira o ano: ")
    
    insert_veiculo(cursor, conection, placa, id_cliente, marca, modelo, cor, ano)

    print("\n--- AGENDAMENTO ---")
    data_agendamento = input("Insira a data e hora do agendamento (Ex: 2025-12-01 10:00): ")
    
    insert_agendamento(cursor, conection, id_cliente, placa, data_agendamento)


def menu_operacoes(cursor, conection, id_cliente):
    """Menu exibido após o login."""
    print(f"\n🔑 Login bem-sucedido! Bem-vindo(a) (ID: {id_cliente})")
    
    while True:
        print("\n--- MENU DE OPERAÇÕES ---")
        print("1. Inserir Veículo e Agendamento")
        print("3. Visualizar serviços")
        print("3.. Logout")
        print("---------------------------")
        
        sub_opcao = input("Escolha uma opção: ")
        
        if sub_opcao == '1':
            fluxo_insercao_operacoes(cursor, conection, id_cliente)
            
        elif sub_opcao == '2':
            print("Saindo da sua conta.")
            break
            
        else:
            print("Opção inválida. Tente novamente.")


def menu_principal(cursor, conection):
    """Exibe o menu principal de acesso ao sistema."""
    while True:
        print("\n" + "="*30)
        print("  SISTEMA DE OFICINA - ACESSO")
        print("="*30)
        print("1. Cadastro (Novo Cliente)")
        print("2. Login (Acessar Conta)")
        print("3. Sair do Programa")
        print("="*30)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            fluxo_cadastro(cursor, conection)
            
        elif opcao == '2':
            print("\n--- LOGIN ---")
            email = input("Email: ")
            senha = input("Senha: ")
            
            id_usuario_logado = fazer_login(cursor, email, senha)
            
            if id_usuario_logado:
                menu_operacoes(cursor, conection, id_usuario_logado)
            
        elif opcao == '3':
            print("Encerrando o sistema. Até logo!")
            break
            
        else:
            print("Opção inválida. Tente novamente.")



def main():
    conection = None
    try:
        conection = conecta()
        cursor = conection.cursor()
        
        menu_principal(cursor, conection)
        
    except Exception as e:
        print(f"\n❌ Ocorreu um erro crítico na aplicação: {e}")
    finally:
        if conection:
            encerra_conexao(conection)

if __name__ == "__main__":
    main()