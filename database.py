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
        print("Conectado com sucesso ao banco 'oficina'.")
        return conn
    except Error as e:
        print(f"Ocorreu um erro ao conectar: {e}")
        return None

def encerra_conexao(conn):
    if conn:
        conn.close()
        print("Conexão com o BD encerrada.")


def criar_tabelas(conn):
    commands = (
        """
        CREATE TABLE clientes(
            id_cliente SERIAL primary key,
            nome varchar(100),
            email varchar(100),
            senha varchar(50)
        );
        """,
        """
        CREATE TABLE tipoServico(
            tipoServico serial primary key,
            nome varchar(100),
            descricao varchar(300)
        );
        """,
        """
        CREATE TABLE mecanico (
            id_mecanico INTEGER PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(50),
            id_gerente INTEGER, 
            CONSTRAINT fk_gerente
                FOREIGN KEY (id_gerente) 
                REFERENCES mecanico(id_mecanico)
        );
        """,
        """
        CREATE TABLE fornecedor(
            id_fornecedor INTEGER primary key,
            nome varchar(100) not null,
            descricao varchar(200)
        );
        """,
        """
        CREATE TABLE veiculo(
            id_veiculo char(7) primary key,
            id_cliente int not null,
            marca varchar(50),
            modelo varchar(100),
            cor varchar(50),
            ano int,
            CONSTRAINT fk_veiculo_cliente
                FOREIGN KEY (id_cliente)
                REFERENCES CLIENTES (id_cliente)
        );
        """,
        """
        CREATE TABLE agendamento(
            id_agendamento SERIAL primary key,
            id_veiculo char(7) not null ,
            data_agendamento TIMESTAMP,
            CONSTRAINT fk_agendamento_veiculo
                FOREIGN KEY (id_veiculo)
                REFERENCES VEICULO (id_veiculo)
        );
        """
    )
    
    cur = None
    try:
        cur = conn.cursor()
        print("Criando tabelas na seguinte ordem:")
        print("1. clientes, 2. tipoServico, 3. mecanico, 4. fornecedor, 5. veiculo, 6. agendamento")
        for command in commands:
            cur.execute(command)
        conn.commit()
        print("Tabelas criadas com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao criar tabelas: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def eliminar_tabelas(conn):
    
    commands = (
        "DROP TABLE IF EXISTS agendamento CASCADE;",
        "DROP TABLE IF EXISTS veiculo CASCADE;",
        "DROP TABLE IF EXISTS clientes CASCADE;",
        "DROP TABLE IF EXISTS tipoServico CASCADE;",
        "DROP TABLE IF EXISTS mecanico CASCADE;",
        "DROP TABLE IF EXISTS fornecedor CASCADE;" 
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


def cadastrar_cliente(conn, nome, email, senha):    
    sql = "INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s);"
    
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (nome, email, senha))
        conn.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar cliente: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()