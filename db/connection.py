import psycopg2
from psycopg2 import OperationalError, Error, DatabaseError

def conecta():
    conn = None
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="1234", 
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
            endereco VARCHAR(200),
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS fornecedor (
            id_fornecedor SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_servico (
            id_tiposervico SERIAL PRIMARY KEY,
            descricao VARCHAR(100),
            nome VARCHAR(100),
            valor DECIMAL(10, 2),
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_pagamento (
            id_tipopagamento SERIAL PRIMARY KEY,
            cnpj VARCHAR(100),
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Faturamento (
            id_faturamento SERIAL PRIMARY KEY,
            valor_total INT,
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
         """
        CREATE TABLE IF NOT EXISTS mecanico (
            id_mecanico SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            cargo VARCHAR(100),
            email VARCHAR(100),
            senha VARCHAR(100),
            fk_mecanico_id_mecanico INT,
            status VARCHAR(20) DEFAULT 'ATIVO'
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
            placa char(7),
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS peca (
            id_peca SERIAL PRIMARY KEY,
            nome_peca VARCHAR(100),
            descricao_peca VARCHAR(100),
            fk_fornecedor_id_fornecedor INT,
            valor_unit DECIMAL(10, 2),
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS agendamento (
            id_agendamento SERIAL PRIMARY KEY,
            data TIMESTAMP,
            fk_veiculo_id_veiculo INT,
            status VARCHAR(20) DEFAULT 'ATIVO'
            
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
            valor_aplicado DECIMAL(10, 2),
            status VARCHAR(20) DEFAULT 'ATIVO'
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
            fk_Faturamento_id_faturamento INT,
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        
        """,
        """
        CREATE TABLE IF NOT EXISTS servico_peca (
            fk_peca_id_peca INT,
            fk_servico_id_servico INT,
            quantidade INT DEFAULT 1,
            status VARCHAR(20) DEFAULT 'ATIVO'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS mecanico_servico (
            fk_mecanico_id_mecanico INT,
            fk_servico_id_servico INT,
            status VARCHAR(20) DEFAULT 'ATIVO'
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
    commands = [
        """
        INSERT INTO cliente (nome, telefone, email, cpf, endereco) VALUES 
        ('João Silva', '11999999999', 'joao@email.com', '11122233344', 'Rua das Flores, 123'),
        ('Maria Oliveira', '21988888888', 'maria@email.com', '55566677788', 'Av. Paulista, 900'),
        ('Pedro Santos', '31977777777', 'pedro@email.com', '99988877766', 'Rua Central, 456'),
        ('Ana Costa', '41966666666', 'ana@email.com', '44455566677', 'Av. Principal, 789'),
        ('Carlos Ferreira', '51955555555', 'carlos@email.com', '33344455566', 'Rua Nova, 321'),
        ('Juliana Lima', '61944444444', 'juliana@email.com', '22233344455', 'Av. Comercial, 654');
        """,
        """
        INSERT INTO fornecedor (nome) VALUES 
        ('Auto Peças Brasil'),
        ('Distribuidora Mecânica Total'),
        ('Peças Premium Ltda'),
        ('Fornecedor Nacional'),
        ('Auto Supply S.A.'),
        ('Distribuidora Central');
        """,
        """
        INSERT INTO tipo_servico (nome, descricao, valor) VALUES 
        ('Troca de Óleo', 'Troca de óleo do motor e filtro', 150.00),
        ('Alinhamento', 'Alinhamento e balanceamento das rodas', 120.00),
        ('Revisão Completa', 'Verificação geral de freios, suspensão e motor', 450.00),
        ('Troca de Pneus', 'Troca e balanceamento de pneus', 200.00),
        ('Reparo de Freios', 'Troca de pastilhas e discos de freio', 350.00),
        ('Troca de Bateria', 'Substituição de bateria automotiva', 250.00);
        """,
        """
        INSERT INTO tipo_pagamento (cnpj) VALUES 
        ('00.000.000/0001-99'),
        ('11.111.111/0001-11'),
        ('22.222.222/0001-22'),
        ('33.333.333/0001-33'),
        ('44.444.444/0001-44'),
        ('55.555.555/0001-55');
        """,
        """
        INSERT INTO mecanico (nome, cargo, email, senha, fk_mecanico_id_mecanico) VALUES 
        ('Carlos Mestre', 'Chefe de Oficina', 'carlos@oficina.com', '1234', NULL),
        ('Pedro Aprendiz', 'Auxiliar', 'pedro@oficina.com','1234', 1),
        ('Roberto Silva', 'Mecânico Especialista', 'roberto@oficina.com','1234', 1),
        ('Fernando Costa', 'Mecânico', 'fernando@oficina.com','1234', 1),
        ('Lucas Alves', 'Auxiliar', 'lucas@oficina.com', '1234', 1),
        ('Marcos Oliveira', 'Mecânico Sênior', 'marcos@oficina.com', '1234', 1);
        """,
        """
        INSERT INTO veiculo (marca, modelo, ano, cor, placa, fk_cliente_id_cliente) VALUES 
        ('Fiat', 'Uno', 2010, 'Prata', 'ABC1234', 1),
        ('Toyota', 'Corolla', 2022, 'Preto', 'XYZ9876', 2),
        ('Volkswagen', 'Gol', 2018, 'Branco', 'DEF5678', 3),
        ('Ford', 'Ka', 2015, 'Vermelho', 'GHI9012', 4),
        ('Chevrolet', 'Onix', 2020, 'Azul', 'JKL3456', 5),
        ('Honda', 'Civic', 2019, 'Prata', 'MNO7890', 6),
        ('Fiat', 'Palio', 2012, 'Preto', 'PQR1234', 1),
        ('Renault', 'Sandero', 2017, 'Branco', 'STU5678', 2);
        """,
        """
        INSERT INTO peca (nome_peca, descricao_peca, fk_fornecedor_id_fornecedor, valor_unit) VALUES 
        ('Filtro de Óleo', 'Filtro padrão universal', 1, 100.00),
        ('Pastilha de Freio', 'Cerâmica', 2, 200.00),
        ('Bateria 60Ah', 'Bateria automotiva 12V', 3, 350.00),
        ('Pneu Aro 15', 'Pneu 185/60 R15', 4, 450.00),
        ('Disco de Freio', 'Disco dianteiro', 5, 280.00),
        ('Filtro de Ar', 'Filtro de ar condicionado', 1, 80.00),
        ('Óleo Motor 5W30', 'Óleo sintético 5L', 2, 120.00),
        ('Amortecedor Dianteiro', 'Amortecedor original', 3, 550.00),
        ('Correia Dentada', 'Correia de distribuição', 4, 180.00),
        ('Radiador', 'Radiador completo', 5, 650.00);
        """,
        """
        INSERT INTO agendamento (data, fk_veiculo_id_veiculo) VALUES 
        ('2025-01-15 08:00:00', 1),
        ('2025-01-16 09:00:00', 2),
        ('2025-01-17 10:00:00', 3),
        ('2025-01-18 11:00:00', 4),
        ('2025-01-19 14:00:00', 5),
        ('2025-01-20 15:00:00', 6),
        ('2025-01-21 08:30:00', 7),
        ('2025-01-22 09:30:00', 8);
        """,
        """
        INSERT INTO servico (descricao, fk_agendamento_id_agendamento, status) VALUES 
        ('Cliente relatou barulho no motor', 1, 'FINALIZADO'),
        ('Revisão periódica solicitada', 2, 'FINALIZADO'),
        ('Problema no sistema de freios', 3, 'FINALIZADO'),
        ('Troca de pneus necessária', 4, 'FINALIZADO'),
        ('Bateria descarregando', 5, 'FINALIZADO'),
        ('Manutenção preventiva', 6, 'EM_ANDAMENTO'),
        ('Reparo na suspensão', 7, 'EM_ANDAMENTO'),
        ('Troca de óleo e filtros', 8, 'ABERTO');
        """,
        """
        INSERT INTO itens_servico (fk_servico_id_servico, fk_tipo_servico_id_tiposervico, valor_aplicado) VALUES 
        (1, 1, 150.00),
        (1, 3, 450.00),
        (2, 3, 450.00),
        (2, 2, 120.00),
        (3, 5, 350.00),
        (3, 1, 150.00),
        (4, 4, 200.00),
        (5, 6, 250.00),
        (5, 1, 150.00),
        (6, 3, 450.00),
        (7, 5, 350.00),
        (8, 1, 150.00);
        """,
        """
        INSERT INTO servico_peca (fk_peca_id_peca, fk_servico_id_servico, quantidade) VALUES 
        (1, 1, 1),
        (2, 3, 2),
        (3, 5, 1),
        (4, 4, 4),
        (5, 3, 2),
        (6, 1, 1),
        (7, 8, 1),
        (8, 7, 2),
        (9, 6, 1),
        (10, 7, 1);
        """,
        """
        INSERT INTO nota_fiscal (valor_pagamento, fk_servico_id_servico, cpf_na_nota, data_emissao) VALUES 
        (600.00, 1, '11122233344', '2025-01-15'),
        (570.00, 2, '55566677788', '2025-01-16'),
        (500.00, 3, '99988877766', '2025-01-17'),
        (200.00, 4, '44455566677', '2025-01-18'),
        (400.00, 5, '33344455566', '2025-01-19');
        """,
        """
        INSERT INTO mecanico_servico (fk_mecanico_id_mecanico, fk_servico_id_servico) VALUES 
        (1, 1),
        (2, 1),
        (3, 2),
        (1, 3),
        (4, 3),
        (5, 4),
        (3, 5),
        (6, 6),
        (2, 7),
        (4, 8);
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

