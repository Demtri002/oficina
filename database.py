import psycopg2
from psycopg2 import OperationalError, Error
from psycopg2 import DatabaseError

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
            id_cliente SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            telefone CHAR(11),
            email VARCHAR(100),
            cpf CHAR(11),
            endereco VARCHAR(200)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS fornecedor (
            id_fornecedor SERIAL PRIMARY KEY,
            nome VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_servico (
            id_tiposervico SERIAL PRIMARY KEY,
            descricao VARCHAR(100),
            nome VARCHAR(100),
            valor DECIMAL(10, 2) -- Preço padrão do serviço
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_pagamento (
            id_tipopagamento SERIAL PRIMARY KEY,
            cnpj VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Faturamento (
            id_faturamento SERIAL PRIMARY KEY,
            valor_total INT
        );
        """,
         """
        CREATE TABLE IF NOT EXISTS mecanico (
            id_mecanico SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            cargo VARCHAR(100),
            email VARCHAR(100),
            fk_mecanico_id_mecanico INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS veiculo (
            id_veiculo SERIAL PRIMARY KEY,
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
            id_peca SERIAL PRIMARY KEY,
            nome_peca VARCHAR(100),
            descricao_peca VARCHAR(100),
            fk_fornecedor_id_fornecedor INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS agendamento (
            id_agendamento SERIAL PRIMARY KEY,
            data TIMESTAMP,
            fk_veiculo_id_veiculo INT
        );
        """,
        """
       CREATE TABLE IF NOT EXISTS servico (
            id_servico SERIAL PRIMARY KEY,
            descricao TEXT,
            data_servico DATE DEFAULT CURRENT_DATE,
            status VARCHAR(20) DEFAULT 'ABERTO', 
            fk_agendamento_id_agendamento INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS itens_servico (
            id_item SERIAL PRIMARY KEY,
            fk_servico_id_servico INT,
            fk_tipo_servico_id_tiposervico INT,
            valor_aplicado DECIMAL(10, 2)
        );
        """,
        """
       
        CREATE TABLE IF NOT EXISTS nota_fiscal (
            id_notafiscal SERIAL PRIMARY KEY,
            valor_pagamento DECIMAL(10, 2),  
            data_emissao DATE DEFAULT CURRENT_DATE, 
            cpf_na_nota CHAR(11),            
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
                    FOREIGN KEY (fk_cliente_id_cliente) REFERENCES cliente (id_cliente) ON DELETE CASCADE;
            END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_agendamento_2') THEN
                ALTER TABLE agendamento ADD CONSTRAINT FK_agendamento_2
                    FOREIGN KEY (fk_veiculo_id_veiculo) REFERENCES veiculo (id_veiculo) ON DELETE CASCADE;
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_agendamento') THEN
                ALTER TABLE servico ADD CONSTRAINT FK_servico_agendamento
                    FOREIGN KEY (fk_agendamento_id_agendamento) REFERENCES agendamento (id_agendamento) ON DELETE CASCADE;
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_item_servico') THEN
                ALTER TABLE itens_servico ADD CONSTRAINT FK_item_servico
                    FOREIGN KEY (fk_servico_id_servico) REFERENCES servico (id_servico) ON DELETE CASCADE;
             END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_item_tipo') THEN
                ALTER TABLE itens_servico ADD CONSTRAINT FK_item_tipo
                    FOREIGN KEY (fk_tipo_servico_id_tiposervico) REFERENCES tipo_servico (id_tiposervico) ON DELETE RESTRICT;
             END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_peca_2') THEN
                ALTER TABLE peca ADD CONSTRAINT FK_peca_2
                    FOREIGN KEY (fk_fornecedor_id_fornecedor) REFERENCES fornecedor (id_fornecedor) ON DELETE CASCADE;
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_nota_fiscal_2') THEN
                ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_2
                    FOREIGN KEY (fk_servico_id_servico) REFERENCES servico (id_servico) ON DELETE CASCADE;
            END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_nota_fiscal_3') THEN
                ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_3
                    FOREIGN KEY (fk_tipo_pagamento_id_tipopagamento) REFERENCES tipo_pagamento (id_tipopagamento) ON DELETE RESTRICT;
             END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_nota_fiscal_4') THEN
                ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_4
                    FOREIGN KEY (fk_Faturamento_id_faturamento) REFERENCES Faturamento (id_faturamento) ON DELETE RESTRICT;
            END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_mecanico_2') THEN
                ALTER TABLE mecanico ADD CONSTRAINT FK_mecanico_2
                    FOREIGN KEY (fk_mecanico_id_mecanico) REFERENCES mecanico (id_mecanico);
            END IF;
        END $$;
        """,

        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_peca_1') THEN
                ALTER TABLE servico_peca ADD CONSTRAINT FK_servico_peca_1
                    FOREIGN KEY (fk_peca_id_peca) REFERENCES peca (id_peca) ON DELETE SET NULL;
            END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_servico_peca_2') THEN
                ALTER TABLE servico_peca ADD CONSTRAINT FK_servico_peca_2
                    FOREIGN KEY (fk_servico_id_servico) REFERENCES servico (id_servico) ON DELETE SET NULL;
             END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_mecanico_servico_1') THEN
                ALTER TABLE mecanico_servico ADD CONSTRAINT FK_mecanico_servico_1
                    FOREIGN KEY (fk_mecanico_id_mecanico) REFERENCES mecanico (id_mecanico) ON DELETE RESTRICT;
            END IF;
        END $$;
        """,
        
        """
        DO $$ BEGIN
             IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_mecanico_servico_2') THEN
                ALTER TABLE mecanico_servico ADD CONSTRAINT FK_mecanico_servico_2
                    FOREIGN KEY (fk_servico_id_servico) REFERENCES servico (id_servico) ON DELETE SET NULL;
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

def inserir_dados_iniciais(conn):
    """
    Popula o banco de dados com dados de teste (Seed).
    """
    commands = [
        # 1. CLIENTES
        """
        INSERT INTO cliente (nome, telefone, email, cpf, endereco) VALUES 
        ('João Silva', '11999999999', 'joao@email.com', '11122233344', 'Rua das Flores, 123'),
        ('Maria Oliveira', '21988888888', 'maria@email.com', '55566677788', 'Av. Paulista, 900');
        """,
        
        # 2. FORNECEDORES
        """
        INSERT INTO fornecedor (nome) VALUES 
        ('Auto Peças Brasil'),
        ('Distribuidora Mecânica Total');
        """,
        
        # 3. TIPOS DE SERVIÇO
        """
        INSERT INTO tipo_servico (nome, descricao, valor) VALUES 
        ('Troca de Óleo', 'Troca de óleo do motor e filtro', 150.00),
        ('Alinhamento', 'Alinhamento e balanceamento das rodas', 120.00),
        ('Revisão Completa', 'Verificação geral de freios, suspensão e motor', 450.00);
        """,
        
        # 4. TIPOS DE PAGAMENTO
        """
        INSERT INTO tipo_pagamento (cnpj) VALUES 
        ('00.000.000/0001-99'), -- Ex: Máquina de Cartão
        ('11.111.111/0001-11');  -- Ex: Transferência Bancária
        """,
        
        # 5. MECÂNICOS
        # O primeiro é o Chefe (Supervisor NULL), o segundo é supervisionado pelo ID 1
        """
        INSERT INTO mecanico (nome, cargo, email, fk_mecanico_id_mecanico) VALUES 
        ('Carlos Mestre', 'Chefe de Oficina', 'carlos@oficina.com', NULL);
        """,
        """
        INSERT INTO mecanico (nome, cargo, email, fk_mecanico_id_mecanico) VALUES 
        ('Pedro Aprendiz', 'Auxiliar', 'pedro@oficina.com', 1); 
        """,

        # 6. VEÍCULOS (Vinculados aos Clientes 1 e 2)
        """
        INSERT INTO veiculo (marca, modelo, ano, cor, placa, fk_cliente_id_cliente) VALUES 
        ('Fiat', 'Uno', 2010, 'Prata', 'ABC1234', 1),
        ('Toyota', 'Corolla', 2022, 'Preto', 'XYZ9876', 2);
        """,

        # 7. PEÇAS (Vinculadas aos Fornecedores 1 e 2)
        """
        INSERT INTO peca (nome_peca, descricao_peca, fk_fornecedor_id_fornecedor) VALUES 
        ('Filtro de Óleo', 'Filtro padrão universal', 1),
        ('Pastilha de Freio', 'Cerâmica', 2);
        """,

        # 8. AGENDAMENTOS (Para os veículos criados)
        """
        INSERT INTO agendamento (data, fk_veiculo_id_veiculo) VALUES 
        ('2025-12-01 08:00:00', 1), -- Agendamento para o Uno
        ('2025-12-02 14:00:00', 2); -- Agendamento para o Corolla
        """,

        # 9. SERVIÇOS (Vinculados aos Agendamentos)
        """
        INSERT INTO servico (descricao, fk_agendamento_id_agendamento) VALUES 
        ('Cliente relatou barulho no motor', 1);
        """,

        # 10. ITENS DO SERVIÇO (Vincula o Serviço 1 aos Tipos de Serviço 1 e 3)
        """
        INSERT INTO itens_servico (fk_servico_id_servico, fk_tipo_servico_id_tiposervico, valor_aplicado) VALUES 
        (1, 1, 150.00), -- Troca de óleo no serviço 1
        (1, 3, 450.00); -- Revisão completa no serviço 1
        """
    ]

    try:
        with conn.cursor() as cur:
            print(" Inserindo dados padrão...")
            for sql in commands:
                cur.execute(sql)
            conn.commit()
            print(" Dados iniciais inseridos com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f" Erro ao inserir dados iniciais: {e}")

def eliminar_tabelas(conn):
    
    commands = (
        "DROP TABLE IF EXISTS itens_servico CASCADE;",   
        "DROP TABLE IF EXISTS mecanico_servico CASCADE;",
        "DROP TABLE IF EXISTS servico_peca CASCADE;",
        "DROP TABLE IF EXISTS nota_fiscal CASCADE;",
        "DROP TABLE IF EXISTS servico CASCADE;",         
        "DROP TABLE IF EXISTS agendamento CASCADE;",
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

def cadastrar_cliente(conn, nome, telefone, email, cpf, endereco):
    sql = """
        INSERT INTO cliente (nome, telefone, email, cpf, endereco)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_cliente;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, telefone, email, cpf, endereco))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Cliente '{nome}' cadastrado com sucesso! ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar cliente: {e}")
        return None

def cadastrar_fornecedor(conn, nome):
    sql = """
        INSERT INTO fornecedor (nome)
        VALUES (%s)
        RETURNING id_fornecedor;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome,))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Fornecedor '{nome}' cadastrado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar fornecedor: {e}")
        return None

def cadastrar_tipo_servico(conn, nome, descricao, valor):
    sql = """
        INSERT INTO tipo_servico (nome, descricao, valor)
        VALUES (%s, %s, %s)
        RETURNING id_tiposervico;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, descricao, valor))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f"Tipo '{nome}' (R$ {valor}) cadastrado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro: {e}")
        return None

def cadastrar_tipo_pagamento(conn, cnpj):
    sql = """
        INSERT INTO tipo_pagamento (cnpj)
        VALUES (%s)
        RETURNING id_tipopagamento;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (cnpj,))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Tipo de Pagamento cadastrado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar tipo de pagamento: {e}")
        return None



def cadastrar_mecanico(conn, nome, cargo, email, id_supervisor=None):
    sql = """
        INSERT INTO mecanico (nome, cargo, email, fk_mecanico_id_mecanico)
        VALUES (%s, %s, %s, %s)
        RETURNING id_mecanico;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cargo, email, id_supervisor))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Mecânico '{nome}' cadastrado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar mecânico: {e}")
        return None

def cadastrar_veiculo(conn, marca, cor, ano, modelo, placa, cpf_cliente):
    
    sql_busca_cliente = "SELECT id_cliente, nome FROM cliente WHERE cpf = %s;"
    
    sql_insert_veiculo = """
        INSERT INTO veiculo (marca, cor, ano, modelo, placa, fk_cliente_id_cliente)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_veiculo;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql_busca_cliente, (cpf_cliente,))
            resultado = cur.fetchone()

            if not resultado:
                print(f" Erro: Nenhum cliente encontrado com o CPF {cpf_cliente}.")
                return None
            
            id_cliente_encontrado = resultado[0]
            nome_cliente = resultado[1]

            cur.execute(sql_insert_veiculo, (marca, cor, ano, modelo, placa, id_cliente_encontrado))
            id_gerado = cur.fetchone()[0]
        
        conn.commit()
        print(f" Veículo '{modelo}' ({placa}) cadastrado para o cliente {nome_cliente}. ID Veículo: {id_gerado}")
        return id_gerado

    except DatabaseError as e:
        conn.rollback()
        print(f" Erro no banco de dados ao cadastrar veículo: {e}")
        return None
    
def cadastrar_peca(conn, nome_peca, descricao_peca, id_fornecedor):
    sql = """
        INSERT INTO peca (nome_peca, descricao_peca, fk_fornecedor_id_fornecedor)
        VALUES (%s, %s, %s)
        RETURNING id_peca;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome_peca, descricao_peca, id_fornecedor))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Peça '{nome_peca}' cadastrada. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f"❌ Erro ao cadastrar peça: {e}")
        return None

def cadastrar_servico(conn, nome, descricao,custo, id_veiculo, id_tipo_servico):
    sql = """
        INSERT INTO servico (nome, descricao, fk_veiculo_id_veiculo, fk_tipo_servico_id_tiposervico)
        VALUES (%s, %s, %s, %s)
        RETURNING id_servico;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, descricao,custo, id_veiculo, id_tipo_servico))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Serviço '{nome}' criado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar serviço: {e}")
        return None

def cadastrar_agendamento(conn, data_hora, placa):
   
    sql_busca_veiculo = "SELECT id_veiculo FROM veiculo WHERE placa = %s;"
    
    sql_insert_agendamento = """
        INSERT INTO agendamento (data, fk_veiculo_id_veiculo)
        VALUES (%s, %s)
        RETURNING id_agendamento;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql_busca_veiculo, (placa,))
            resultado = cur.fetchone()

            if not resultado:
                print(f"Erro: Veículo com placa '{placa}' não encontrado.")
                return None
            
            id_veiculo_encontrado = resultado[0]

            cur.execute(sql_insert_agendamento, (data_hora, id_veiculo_encontrado))
            id_gerado = cur.fetchone()[0]
        
        conn.commit()
        print(f"Agendamento realizado para o veículo {placa} em {data_hora}. ID Agendamento: {id_gerado}")
        return id_gerado

    except DatabaseError as e:
        conn.rollback()
        print(f"Erro ao cadastrar agendamento: {e}")
        return None




def vincular_servico_peca(conn, id_peca, id_servico):
    sql = """
        INSERT INTO servico_peca (fk_peca_id_peca, fk_servico_id_servico)
        VALUES (%s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_peca, id_servico))
        conn.commit()
        print(f" Peça ID {id_peca} vinculada ao Serviço ID {id_servico}.")
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao vincular peça ao serviço: {e}")


def vincular_mecanico_servico(conn, id_mecanico, id_servico):
    sql = """
        INSERT INTO mecanico_servico (fk_mecanico_id_mecanico, fk_servico_id_servico)
        VALUES (%s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_mecanico, id_servico))
        conn.commit()
        print(f" Mecânico ID {id_mecanico} vinculado ao Serviço ID {id_servico}.")
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao vincular mecânico ao serviço: {e}")

def listar_clientes(conn):
    sql = "SELECT id_cliente, nome, telefone, email, cpf, endereco FROM cliente ORDER BY id_cliente;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            clientes = cur.fetchall()
            print("\n--- Lista de Clientes ---")
            for cliente in clientes:
                print(f"ID: {cliente[0]}, Nome: {cliente[1]}, Telefone: {cliente[2]}, Email: {cliente[3]}, CPF: {cliente[4]}, Endereço: {cliente[5]}")
    except DatabaseError as e:
        print(f" Erro ao listar clientes: {e}")

def listar_veiculos(conn):
    sql = "SELECT id_veiculo, marca, modelo, placa, ano, cor, fk_cliente_id_cliente FROM veiculo ORDER BY id_veiculo;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            veiculos = cur.fetchall()
            print("\n--- Lista de Veículos ---")
            for veiculo in veiculos:
                print(f"ID: {veiculo[0]}, Marca: {veiculo[1]}, Modelo: {veiculo[2]}, Placa: {veiculo[3]}, Ano: {veiculo[4]}, Cor: {veiculo[5]}, ID Cliente: {veiculo[6]}")
    except DatabaseError as e:
        print(f" Erro ao listar veículos: {e}")

def listar_mecanicos(conn):
    sql = "SELECT id_mecanico, nome, cargo, email, fk_mecanico_id_mecanico FROM mecanico ORDER BY id_mecanico;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            mecanicos = cur.fetchall()
            print("\n--- Lista de Mecânicos ---")
            for mecanico in mecanicos:
                print(f"ID: {mecanico[0]}, Nome: {mecanico[1]}, Cargo: {mecanico[2]}, Email: {mecanico[3]}, ID Supervisor: {mecanico[4]}")
    except DatabaseError as e:
        print(f" Erro ao listar mecânicos: {e}")

def listar_fornecedores(conn):
    sql = "SELECT id_fornecedor, nome FROM fornecedor ORDER BY id_fornecedor;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            fornecedores = cur.fetchall()
            print("\n--- Lista de Fornecedores ---")
            for fornecedor in fornecedores:
                print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}")
    except DatabaseError as e:
        print(f" Erro ao listar fornecedores: {e}")

def listar_agendamentos(conn):
    sql = "SELECT id_agendamento, data, fk_veiculo_id_veiculo FROM agendamento ORDER BY id_agendamento;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            agendamentos = cur.fetchall()
            print("\n--- Lista de Agendamentos ---")
            for agendamento in agendamentos:
                print(f"ID: {agendamento[0]}, Data: {agendamento[1]}, ID Veículo: {agendamento[2]}")
    except DatabaseError as e:
        print(f" Erro ao listar agendamentos: {e}")

def buscar_agendamento_detalhado(conn, id_agendamento):
    sql = """
        SELECT a.data, v.modelo, v.placa, c.nome
        FROM agendamento a
        JOIN veiculo v ON a.fk_veiculo_id_veiculo = v.id_veiculo
        JOIN cliente c ON v.fk_cliente_id_cliente = c.id_cliente
        WHERE a.id_agendamento = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_agendamento,))
            res = cur.fetchone()
            return res 
    except DatabaseError:
        return None

def abrir_ordem_servico(conn, id_agendamento, descricao):
    sql = """
        INSERT INTO servico (fk_agendamento_id_agendamento, descricao)
        VALUES (%s, %s)
        RETURNING id_servico;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_agendamento, descricao))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Ordem de Serviço #{id_gerado} aberta!")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao abrir serviço: {e}")
        return None

def adicionar_nota_fiscal(conn, id_nota_fiscal, id_tipo_servico):
    """
    Adiciona um item (serviço) a uma Nota Fiscal específica, puxando o valor atual do tipo de serviço.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT valor, nome FROM tipo_servico WHERE id_tiposervico = %s", (id_tipo_servico,))
            res = cur.fetchone()
            
            if not res:
                print(" Tipo de serviço não encontrado.")
                return False
            
            valor_atual, nome_servico = res
            
           
            sql_insert = """
                INSERT INTO itens_nota_fiscal (fk_nota_fiscal_id, fk_tipo_servico_id_tiposervico, valor_cobrado)
                VALUES (%s, %s, %s);
            """
            
            cur.execute(sql_insert, (id_nota_fiscal, id_tipo_servico, valor_atual))
            conn.commit()
            
            print(f" Item '{nome_servico}' adicionado à NF {id_nota_fiscal} (R$ {valor_atual}).")
            return True

    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao adicionar item na nota: {e}")
        return False

def calcular_valor_total_servico(conn, id_servico):
    sql = """
        SELECT SUM(valor_aplicado) FROM itens_servico
        WHERE fk_servico_id_servico = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_servico,))
            total = cur.fetchone()[0]
            return total if total else 0
    except DatabaseError as e:
        print(f" Erro ao calcular valor total: {e}")
        return 0

def listar_servicos_simples(conn):
    sql = "SELECT id_tiposervico, nome, descricao, valor FROM tipo_servico ORDER BY id_tiposervico;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            servicos = cur.fetchall()
            print("\n--- Tipos de Serviços Disponíveis ---")
            for servico in servicos:
                print(f"ID: {servico[0]}, Nome: {servico[1]}, Descrição: {servico[2]}, Valor: R$ {servico[3]:.2f}")
    except DatabaseError as e:
        print(f" Erro ao listar tipos de serviço: {e}")

def consultar_faturamento_por_periodo(conn, data_inicio, data_fim):
    
    sql = """
        SELECT 
            SUM(valor_pagamento) AS total_faturado,
            COUNT(id_notafiscal) AS total_notas
        FROM nota_fiscal
        WHERE data_emissao >= %s AND data_emissao <= %s;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (data_inicio, data_fim))
            resultado = cur.fetchone()
            
            total, num_notas = resultado
            
            if total is None:
                total = 0.00
                
            print(f"\n===  Relatório Financeiro ===")
            print(f" Período: {data_inicio} até {data_fim}")
            print(f" Quantidade de Notas Emitidas: {num_notas}")
            print(f" Faturamento Total: R$ {total:.2f}")
            print("===============================")
            
            return total
            
    except DatabaseError as e:
        print(f"❌ Erro ao consultar faturamento: {e}")
        return None


def cadastrar_nota_fiscal(conn, valor_pagamento, id_servico, id_tipo_pagamento, id_faturamento):
    sql = """
        INSERT INTO nota_fiscal (valor_pagamento, fk_servico_id_servico, fk_tipo_pagamento_id_tipopagamento, fk_Faturamento_id_faturamento)
        VALUES (%s, %s, %s, %s)
        RETURNING id_notafiscal;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (valor_pagamento, id_servico, id_tipo_pagamento, id_faturamento))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Nota Fiscal gerada. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao gerar nota fiscal: {e}")
        return None

def finalizar_servico_gerar_nf(conn, id_servico):
    """
    Finaliza o serviço, soma os itens, percorre Agendamento -> Veículo -> Cliente
    para pegar o CPF e gera a Nota Fiscal.
    """
    try:
        with conn.cursor() as cur:
            sql_consulta = """
                SELECT 
                    c.cpf,
                    SUM(i.valor_aplicado) as total_servico
                FROM servico s
                -- O Serviço está ligado ao Agendamento
                JOIN agendamento a ON s.fk_agendamento_id_agendamento = a.id_agendamento
                -- O Agendamento está ligado ao Veículo
                JOIN veiculo v ON a.fk_veiculo_id_veiculo = v.id_veiculo
                -- O Veículo está ligado ao Cliente (ONDE ESTÁ O CPF!)
                JOIN cliente c ON v.fk_cliente_id_cliente = c.id_cliente
                -- Pegamos os itens do serviço para somar
                LEFT JOIN itens_servico i ON i.fk_servico_id_servico = s.id_servico
                WHERE s.id_servico = %s
                GROUP BY c.cpf;
            """
            
            cur.execute(sql_consulta, (id_servico,))
            res = cur.fetchone()
            
            if not res:
                print(" Erro: Serviço não encontrado ou cadeia de relacionamentos (Agendamento/Veículo/Cliente) quebrada.")
                return False
            
            cpf_cliente, valor_total = res
            
            if valor_total is None:
                valor_total = 0.0
            
            if not cpf_cliente:
                print(" Aviso: Cliente sem CPF cadastrado.")
                cpf_cliente = None 

          
            sql_insert_nf = """
                INSERT INTO nota_fiscal (fk_servico_id_servico, cpf_na_nota, valor_pagamento, data_emissao)
                VALUES (%s, %s, %s, CURRENT_DATE)
                RETURNING id_notafiscal;
            """
            
            
            cur.execute(sql_insert_nf, (id_servico, cpf_cliente, valor_total))
            id_nova_nf = cur.fetchone()[0]

            
            conn.commit()
            print(f" Serviço Finalizado com Sucesso!")
            print(f" Nota Fiscal Gerada: ID {id_nova_nf}")
            print(f" CPF na Nota: {cpf_cliente}")
            print(f" Valor Total: R$ {valor_total:.2f}")
            return True

    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao gerar Nota Fiscal: {e}")
        return False
    
def adicionar_item_servico(conn, id_servico, id_tipo_servico):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT valor, nome FROM tipo_servico WHERE id_tiposervico = %s", (id_tipo_servico,))
            res = cur.fetchone()
            
            if not res:
                print(" Tipo de serviço não encontrado.")
                return False
            
            valor_padrao, nome_servico = res
            
            sql_insert = """
                INSERT INTO itens_servico (fk_servico_id_servico, fk_tipo_servico_id_tiposervico, valor_aplicado)
                VALUES (%s, %s, %s);
            """
            cur.execute(sql_insert, (id_servico, id_tipo_servico, valor_padrao))
            conn.commit()
            
            print(f" Item '{nome_servico}' adicionado ao serviço (Valor: R$ {valor_padrao}).")
            return True
            
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao adicionar item: {e}")
        return False
    
def iniciar_servico(conn, id_servico):

    sql = "UPDATE servico SET status = 'EM_ANDAMENTO' WHERE id_servico = %s AND status = 'ABERTO'"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_servico,))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Serviço {id_servico} iniciado e status alterado para 'EM_ANDAMENTO'.")
                return True
            else:
                print(f" Serviço {id_servico} não está no status 'ABERTO' ou não existe. Status não alterado.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f"❌ Erro ao iniciar serviço: {e}")
        return False

def listar_servicos_em_andamento(conn):
   
    sql = """
        SELECT s.id_servico, s.data_servico, c.nome AS cliente, v.placa
        FROM servico s
        JOIN agendamento a ON s.fk_agendamento_id_agendamento = a.id_agendamento
        JOIN veiculo v ON a.fk_veiculo_id_veiculo = v.id_veiculo
        JOIN cliente c ON v.fk_cliente_id_cliente = c.id_cliente
        WHERE s.status = 'EM_ANDAMENTO';
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            servicos = cur.fetchall()
            
            if not servicos:
                print("\n Não há serviços em 'EM_ANDAMENTO' no momento.")
                return []

            print("\n---  Serviços EM ANDAMENTO ---")
            print("{:<5} | {:<10} | {:<30} | {:<7}".format("ID", "Data", "Cliente", "Placa"))
            print("-" * 55)
            for s in servicos:
                print("{:<5} | {:<10} | {:<30} | {:<7}".format(s[0], s[1].strftime("%Y-%m-%d"), s[2], s[3]))
            print("-" * 55)
            return servicos
            
    except DatabaseError as e:
        print(f" Erro ao listar serviços: {e}")
        return []
    
def listar_servicos_finalizados(conn):
   
    sql = """
        SELECT s.id_servico, s.data_servico, c.nome AS cliente, v.placa
        FROM servico s
        JOIN agendamento a ON s.fk_agendamento_id_agendamento = a.id_agendamento
        JOIN veiculo v ON a.fk_veiculo_id_veiculo = v.id_veiculo
        JOIN cliente c ON v.fk_cliente_id_cliente = c.id_cliente
        WHERE s.status = 'FINALIZADO';
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            servicos = cur.fetchall()
            
            if not servicos:
                print("\n Não há serviços 'FINALIZADOS' no momento.")
                return []

            print("\n---  Serviços FINALIZADOS ---")
            print("{:<5} | {:<10} | {:<30} | {:<7}".format("ID", "Data", "Cliente", "Placa"))
            print("-" * 55)
            for s in servicos:
                print("{:<5} | {:<10} | {:<30} | {:<7}".format(s[0], s[1].strftime("%Y-%m-%d"), s[2], s[3]))
            print("-" * 55)
            return servicos
            
    except DatabaseError as e:
        print(f" Erro ao listar serviços: {e}")
        return []