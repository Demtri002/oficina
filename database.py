import psycopg2
from psycopg2 import OperationalError, Error


def conecta():
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
    if conn:
        conn.close()


def criar_tabelas(conn):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INT PRIMARY KEY,
            nome VARCHAR(100),
            telefone CHAR(11),
            email VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS fornecedor (
            id_fornecedor INT PRIMARY KEY,
            nome VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_servico (
            id_tiposervico INT PRIMARY KEY,
            descricao VARCHAR(100),
            nome VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_pagamento (
            id_tipopagamento INT PRIMARY KEY,
            cnpj VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Faturamento (
            id_faturamento INT PRIMARY KEY,
            valor_total INT
        );
        """,
         """
        CREATE TABLE IF NOT EXISTS mecanico (
            id_mecanico INT PRIMARY KEY,
            nome VARCHAR(100),
            cargo VARCHAR(100),
            email VARCHAR(100),
            fk_mecanico_id_mecanico INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS veiculo (
            id_veiculo INT PRIMARY KEY,
            marca VARCHAR(100),
            cor VARCHAR(100),
            ano INT,
            modelo VARCHAR(100),
            fk_cliente_id_cliente INT,
            placa char(7)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS peca (
            id_peca INT PRIMARY KEY,
            nome_peca VARCHAR(100),
            descricao_peca VARCHAR(100),
            fk_fornecedor_id_fornecedor INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS servico (
            id_servico INT PRIMARY KEY,
            nome VARCHAR(100),
            descricao VARCHAR(100),
            fk_veiculo_id_veiculo INT,
            fk_tipo_servico_id_tiposervico INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS agendamento (
            id_agendamento INT PRIMARY KEY,
            data TIMESTAMP,
            fk_veiculo_id_veiculo INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS nota_fiscal (
            id_notafiscal INT PRIMARY KEY,
            valor_pagamento INT,
            fk_servico_id_servico INT,
            fk_tipo_pagamento_id_tipopagamento INT,
            fk_Faturamento_id_faturamento INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS servico_peca (
            fk_peca_id_peca INT,
            fk_servico_id_servico INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS mecanico_servico (
            fk_mecanico_id_mecanico INT,
            fk_servico_id_servico INT
        );
        """,
     
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_veiculo_2') THEN
                ALTER TABLE veiculo ADD CONSTRAINT FK_veiculo_2
                    FOREIGN KEY (fk_cliente_id_cliente)
                    REFERENCES cliente (id_cliente)
                    ON DELETE CASCADE;
            END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_2') THEN
                ALTER TABLE servico ADD CONSTRAINT FK_servico_2
                    FOREIGN KEY (fk_veiculo_id_veiculo)
                    REFERENCES veiculo (id_veiculo)
                    ON DELETE CASCADE;
            END IF;
        END $$;
        """,
        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_3') THEN
                ALTER TABLE servico ADD CONSTRAINT FK_servico_3
                    FOREIGN KEY (fk_tipo_servico_id_tiposervico)
                    REFERENCES tipo_servico (id_tiposervico)
                    ON DELETE CASCADE;
             END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_peca_2') THEN
                ALTER TABLE peca ADD CONSTRAINT FK_peca_2
                    FOREIGN KEY (fk_fornecedor_id_fornecedor)
                    REFERENCES fornecedor (id_fornecedor)
                    ON DELETE CASCADE;
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_nota_fiscal_2') THEN
                ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_2
                    FOREIGN KEY (fk_servico_id_servico)
                    REFERENCES servico (id_servico)
                    ON DELETE CASCADE;
            END IF;
        END $$;
        """,
        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_nota_fiscal_3') THEN
                ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_3
                    FOREIGN KEY (fk_tipo_pagamento_id_tipopagamento)
                    REFERENCES tipo_pagamento (id_tipopagamento)
                    ON DELETE RESTRICT;
             END IF;
        END $$;
        """,
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_nota_fiscal_4') THEN
                ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_4
                    FOREIGN KEY (fk_Faturamento_id_faturamento)
                    REFERENCES Faturamento (id_faturamento)
                    ON DELETE RESTRICT;
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_mecanico_2') THEN
                ALTER TABLE mecanico ADD CONSTRAINT FK_mecanico_2
                    FOREIGN KEY (fk_mecanico_id_mecanico)
                    REFERENCES mecanico (id_mecanico);
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_agendamento_2') THEN
                ALTER TABLE agendamento ADD CONSTRAINT FK_agendamento_2
                    FOREIGN KEY (fk_veiculo_id_veiculo)
                    REFERENCES veiculo (id_veiculo)
                    ON DELETE CASCADE;
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_peca_1') THEN
                ALTER TABLE servico_peca ADD CONSTRAINT FK_servico_peca_1
                    FOREIGN KEY (fk_peca_id_peca)
                    REFERENCES peca (id_peca)
                    ON DELETE SET NULL;
            END IF;
        END $$;
        """,
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_peca_2') THEN
                ALTER TABLE servico_peca ADD CONSTRAINT FK_servico_peca_2
                    FOREIGN KEY (fk_servico_id_servico)
                    REFERENCES servico (id_servico)
                    ON DELETE SET NULL;
             END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_mecanico_servico_1') THEN
                ALTER TABLE mecanico_servico ADD CONSTRAINT FK_mecanico_servico_1
                    FOREIGN KEY (fk_mecanico_id_mecanico)
                    REFERENCES mecanico (id_mecanico)
                    ON DELETE RESTRICT;
            END IF;
        END $$;
        """,
        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_mecanico_servico_2') THEN
                ALTER TABLE mecanico_servico ADD CONSTRAINT FK_mecanico_servico_2
                    FOREIGN KEY (fk_servico_id_servico)
                    REFERENCES servico (id_servico)
                    ON DELETE SET NULL;
             END IF;
        END $$;
        """
    )
    
    cur = None
    try:
        cur = conn.cursor()
        print("Verificando/Criando tabelas e constraints...")
        for command in commands:
            cur.execute(command)
        conn.commit()
        print("Estrutura de tabelas (Lógico_2) verificada com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao criar tabelas: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()



def eliminar_tabelas(conn):
    
    commands = (
        "DROP TABLE IF EXISTS mecanico_servico CASCADE;",
        "DROP TABLE IF EXISTS servico_peca CASCADE;",
        "DROP TABLE IF EXISTS nota_fiscal CASCADE;",
        "DROP TABLE IF EXISTS agendamento CASCADE;",
        "DROP TABLE IF EXISTS servico CASCADE;",
        "DROP TABLE IF EXISTS peca CASCADE;",
        "DROP TABLE IF EXISTS veiculo CASCADE;",
        "DROP TABLE IF EXISTS mecanico CASCADE;",
        "DROP TABLE IF EXISTS Faturamento CASCADE;",
        "DROP TABLE IF EXISTS tipo_pagamento CASCADE;",
        "DROP TABLE IF EXISTS tipo_servico CASCADE;",
        "DROP TABLE IF EXISTS fornecedor CASCADE;",
        "DROP TABLE IF EXISTS cliente CASCADE;"
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
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_cliente, nome FROM clientes WHERE cpf = %s;", (cpf,))
            resultado = cur.fetchone() 
            return resultado
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao buscar cliente: {error}")
        return None

def buscar_veiculo_por_placa(conn, placa):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM veiculo WHERE placa = %s;", (placa,))
            return cur.fetchone() is not None
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao buscar veículo: {error}")
        return False
        
def listar_servicos_simples(conn):
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