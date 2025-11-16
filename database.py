import psycopg2
from psycopg2 import OperationalError, Error


def conecta():
    """Tenta conectar ao banco de dados PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="1010", 
            host="localhost",
            port="5432",
            database="oficina"
        )
        return conn
    except OperationalError as e:
        if "database \"oficina\" does not exist" in str(e):
            print("Banco 'oficina' não encontrado. Crie-o manualmente no PostgreSQL.")
        else:
            print(f"Ocorreu um erro ao conectar: {e}")
        return None
    except Error as e:
        print(f"Ocorreu um erro ao conectar: {e}")
        return None

def encerra_conexao(conn):
    """Encerra a conexão com o banco de dados, se estiver ativa."""
    if conn:
        conn.close()


def criar_tabelas(conn):
    """
    Cria a estrutura de tabelas no banco de dados. 
    Usa 'CREATE TABLE IF NOT EXISTS' para rodar sem erros.
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS clientes(
            id_cliente SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cpf VARCHAR(14) UNIQUE NOT NULL,
            endereco VARCHAR(200),
            telefone VARCHAR(20)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS mecanico (
            id_mecanico SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipoServico(
            id_tipoServico SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao VARCHAR(300),
            valor_padrao DECIMAL(10, 2)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS veiculo(
            placa CHAR(7) PRIMARY KEY,
            id_cliente INT NOT NULL,
            marca VARCHAR(50),
            modelo VARCHAR(100),
            ano INT,
            cor VARCHAR(50),
            CONSTRAINT fk_veiculo_cliente
                FOREIGN KEY (id_cliente)
                REFERENCES clientes (id_cliente)
                ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS agendamento(
            id_agendamento SERIAL PRIMARY KEY,
            placa CHAR(7) NOT NULL,
            id_tipoServico INT NOT NULL,
            data_agendamento TIMESTAMP NOT NULL,
            status VARCHAR(50) DEFAULT 'Agendado', 
            CONSTRAINT fk_agendamento_veiculo
                FOREIGN KEY (placa)
                REFERENCES veiculo (placa)
                ON DELETE CASCADE,
            CONSTRAINT fk_agendamento_servico
                FOREIGN KEY (id_tipoServico)
                REFERENCES tipoServico (id_tipoServico)
        );
        """
    )
    
    cur = None
    try:
        cur = conn.cursor()
        print("Verificando/Criando tabelas...")
        for command in commands:
            cur.execute(command)
        conn.commit()
        print("Estrutura de tabelas verificada com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao criar tabelas: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def eliminar_tabelas(conn):
    """Elimina (DROP) todas as tabelas. APENAS PARA TESTES."""
    commands = (
        "DROP TABLE IF EXISTS agendamento CASCADE;",
        "DROP TABLE IF EXISTS veiculo CASCADE;",
        "DROP TABLE IF EXISTS clientes CASCADE;",
        "DROP TABLE IF EXISTS tipoServico CASCADE;",
        "DROP TABLE IF EXISTS mecanico CASCADE;"
    )
    cur = None
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        print("Tabelas eliminadas com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao eliminar tabelas: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()


def cadastrar_cliente(conn, nome, cpf, endereco, telefone):
    sql = "INSERT INTO clientes (nome, cpf, endereco, telefone) VALUES (%s, %s, %s, %s);"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cpf, endereco, telefone))
        conn.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar cliente: {error}")
        conn.rollback()

def cadastrar_veiculo(conn, placa, id_cliente, marca, modelo):
    sql = "INSERT INTO veiculo (placa, id_cliente, marca, modelo) VALUES (%s, %s, %s, %s);"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (placa, id_cliente, marca, modelo))
        conn.commit()
        print(f"Veículo placa '{placa}' cadastrado com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar veículo: {error}")
        conn.rollback()

def cadastrar_agendamento(conn, placa, id_tipoServico, data):
    sql = "INSERT INTO agendamento (placa, id_tipoServico, data_agendamento) VALUES (%s, %s, %s);"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (placa, id_tipoServico, data))
        conn.commit()
        print(f"Agendamento para '{placa}' em {data} cadastrado com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar agendamento: {error}")
        conn.rollback()
        
def cadastrar_mecanico(conn, nome, cargo):
    sql = "INSERT INTO mecanico (nome, cargo) VALUES (%s, %s);"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cargo))
        conn.commit()
        print(f"Mecânico '{nome}' cadastrado com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar mecânico: {error}")
        conn.rollback()


def cadastrar_tipo_servico(conn, nome, valor):    
    sql = "INSERT INTO tipoServico (nome, valor_padrao) VALUES (%s, %s);"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, valor))
        conn.commit()
        print(f"Serviço '{nome}' (R$ {valor}) cadastrado com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar tipo de serviço: {error}")
        conn.rollback()

def listar_clientes(conn):
    sql = "SELECT id_cliente, nome, cpf, telefone FROM clientes ORDER BY nome;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            resultados = cur.fetchall() 
            if not resultados:
                print("Nenhum cliente cadastrado.")
                return
            
            print("\n--- Lista de Clientes ---")
            for cliente in resultados:
                print(f"ID: {cliente[0]}, Nome: {cliente[1]}, CPF: {cliente[2]}, Tel: {cliente[3]}")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar clientes: {error}")

def listar_veiculos(conn):
    sql = """
        SELECT v.placa, v.marca, v.modelo, c.nome as dono
        FROM veiculo v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        ORDER BY dono, v.modelo;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhum veículo cadastrado.")
                return
                
            print("\n--- Lista de Veículos ---")
            for veiculo in resultados:
                print(f"Placa: {veiculo[0]}, Modelo: {veiculo[1]} {veiculo[2]}, Dono: {veiculo[3]}")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar veículos: {error}")

def listar_agendamentos(conn):
    sql = """
        SELECT a.id_agendamento, a.data_agendamento, a.status, v.placa, v.modelo, ts.nome as servico
        FROM agendamento a
        JOIN veiculo v ON a.placa = v.placa
        JOIN tipoServico ts ON a.id_tipoServico = ts.id_tipoServico
        WHERE a.status = 'Agendado'
        ORDER BY a.data_agendamento;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhum agendamento futuro encontrado.")
                return
            
            print("\n--- Próximos Agendamentos ---")
            for ag in resultados:
                print(f"ID: {ag[0]}, Data: {ag[1]}, Status: {ag[2]}, Veículo: {ag[3]} ({ag[4]}), Serviço: {ag[5]}")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar agendamentos: {error}")
        
def listar_servicos_realizados(conn):
    print("FUNCIONALIDADE 'Serviços Realizados' AINDA NÃO IMPLEMENTADA.")

def consultar_faturamento_mensal(conn):
    print("FUNCIONALIDADE 'Faturamento' AINDA NÃO IMPLEMENTADA.")
  

def atualizar_cliente(conn, id_cliente, nome, cpf, endereco, telefone):
    sql = """
        UPDATE clientes
        SET nome = %s, cpf = %s, endereco = %s, telefone = %s
        WHERE id_cliente = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cpf, endereco, telefone, id_cliente))
        conn.commit()
        print(f"Cadastro do cliente ID {id_cliente} atualizado!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao atualizar cliente: {error}")
        conn.rollback()

def atualizar_mecanico(conn, id_mecanico, nome, cargo):
    sql = "UPDATE mecanico SET nome = %s, cargo = %s WHERE id_mecanico = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cargo, id_mecanico))
        conn.commit()
        print(f"Cadastro do mecânico ID {id_mecanico} atualizado!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao atualizar mecânico: {error}")
        conn.rollback()


def buscar_cliente_por_cpf(conn, cpf):
    """Busca um cliente pelo CPF e retorna seu ID e Nome. Retorna None se não achar."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_cliente, nome FROM clientes WHERE cpf = %s;", (cpf,))
            resultado = cur.fetchone() 
            return resultado
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao buscar cliente: {error}")
        return None

def buscar_veiculo_por_placa(conn, placa):
    """Verifica se uma placa existe. Retorna True se existir."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM veiculo WHERE placa = %s;", (placa,))
            return cur.fetchone() is not None
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao buscar veículo: {error}")
        return False
        
def listar_servicos_simples(conn):
    """Lista serviços (ID, Nome, Valor) para seleção no menu."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_tipoServico, nome, valor_padrao FROM tipoServico ORDER BY nome;")
            resultados = cur.fetchall()
            if not resultados:
                print("Nenhum tipo de serviço cadastrado.")
                return None
            print("\n--- Tipos de Serviço Disponíveis ---")
            for servico in resultados:
                print(f"ID: {servico[0]}, Nome: {servico[1]}, Valor: R${servico[2]}")
            return resultados
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao listar serviços: {error}")
        return None