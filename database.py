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
        CREATE TABLE Clientes (
            cliente_id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(20)
        );
        """,
        """
        CREATE TABLE Veiculos (
            veiculo_id SERIAL PRIMARY KEY,
            placa VARCHAR(10) NOT NULL UNIQUE,
            modelo VARCHAR(50),
            ano INTEGER,
            cliente_id INTEGER,
            FOREIGN KEY (cliente_id)
                REFERENCES Clientes (cliente_id)
                ON DELETE SET NULL
        );
        """,
        """
        CREATE TABLE Servicos (
            servico_id SERIAL PRIMARY KEY,
            veiculo_id INTEGER NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            data DATE NOT NULL DEFAULT CURRENT_DATE,
            valor DECIMAL(10, 2),
            FOREIGN KEY (veiculo_id)
                REFERENCES Veiculos (veiculo_id)
                ON DELETE CASCADE
        );
        """
    )
    
    cur = None
    try:
        cur = conn.cursor()
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
        "DROP TABLE IF EXISTS Servicos CASCADE;",
        "DROP TABLE IF EXISTS Veiculos CASCADE;",
        "DROP TABLE IF EXISTS Clientes CASCADE;"
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


def cadastrar_cliente(conn, nome, telefone):
    
    sql = "INSERT INTO Clientes (nome, telefone) VALUES (%s, %s);"
    
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (nome, telefone))
        conn.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao cadastrar cliente: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()