
#  Tabela cliente
create table clientes(
	id_cliente SERIAL primary key,
	nome varchar(100),
	email varchar(100),
	senha varchar(50)
);

# Tabela Veiculo

create table veiculo(
	id_veiculo char(7) primary key,
	id_cliente int not null,
	marca varchar(50),
	modelo varchar(100),
	cor varchar(50),
	ano int,
	CONSTRAINT fk_veiculo_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES CLIENTES (id_cliente)
)

# Tabela Agendamento 

create table agendamento(
	id_agendamento SERIAL primary key,
	id_veiculo char(7) not null ,
	data_agendamento TIMESTAMP,
	CONSTRAINT fk_agendamento_veiculo
        FOREIGN KEY (id_veiculo)
        REFERENCES VEICULO (id_veiculo)
	
	)

# Tabela Tipo de servico

create table tipoServico(
	tipoServico serial primary key,
	nome varchar(100),
	descricao varchar(300)
)

# Tabela Mecanico

CREATE TABLE mecanico (
    id_mecanico INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    id_gerente INTEGER, 
    CONSTRAINT fk_gerente
        FOREIGN KEY (id_gerente) 
        REFERENCES mecanico(id_mecanico)
);

# Tabela fornecedor 

CREATE TABLE forncedor(
	id_forncedor INTEGER primary key,
	nome varchar(100) not null,
	descricao varchar(200)
);



/* Lógico_2: */

CREATE TABLE cliente (
    id_cliente INT PRIMARY KEY,
    nome VARCHAR(100),
    telefone CHAR(11),
    email VARCHAR(100)
);

CREATE TABLE veiculo (
    id_veiculo INT PRIMARY KEY,
    marca VARCHAR(100),
    cor VARCHAR(100),
    ano INT,
    modelo VARCHAR(100),
    fk_cliente_id_cliente INT,
    placa char(7)
);

CREATE TABLE servico (
    id_servico INT PRIMARY KEY,
    nome VARCHAR(100),
    descricao VARCHAR(100),
    fk_veiculo_id_veiculo INT,
    fk_tipo_servico_id_tiposervico INT
);

CREATE TABLE tipo_servico (
    id_tiposervico INT PRIMARY KEY,
    descricao VARCHAR(100),
    nome VARCHAR(100)
);

CREATE TABLE peca (
    id_peca INT PRIMARY KEY,
    nome_peca VARCHAR(100),
    descricao_peca VARCHAR(100),
    fk_fornecedor_id_fornecedor INT
);

CREATE TABLE nota_fiscal (
    id_notafiscal INT PRIMARY KEY,
    valor_pagamento INT,
    fk_servico_id_servico INT,
    fk_tipo_pagamento_id_tipopagamento INT,
    fk_Faturamento_id_faturamento INT
);

CREATE TABLE mecanico (
    id_mecanico INT PRIMARY KEY,
    nome VARCHAR(100),
    cargo VARCHAR(100),
    email VARCHAR(100),
    fk_mecanico_id_mecanico INT
);

CREATE TABLE fornecedor (
    id_fornecedor INT PRIMARY KEY,
    nome VARCHAR(100)
);

CREATE TABLE agendamento (
    id_agendamento INT PRIMARY KEY,
    data TIMESTAMP,
    fk_veiculo_id_veiculo INT
);

CREATE TABLE tipo_pagamento (
    id_tipopagamento INT PRIMARY KEY,
    cnpj VARCHAR(100)
);

CREATE TABLE Faturamento (
    id_faturamento INT PRIMARY KEY,
    valor_total INT
);

CREATE TABLE servico_peca (
    fk_peca_id_peca INT,
    fk_servico_id_servico INT
);

CREATE TABLE mecanico_servico (
    fk_mecanico_id_mecanico INT,
    fk_servico_id_servico INT
);
 
ALTER TABLE veiculo ADD CONSTRAINT FK_veiculo_2
    FOREIGN KEY (fk_cliente_id_cliente)
    REFERENCES cliente (id_cliente)
    ON DELETE CASCADE;
 
ALTER TABLE servico ADD CONSTRAINT FK_servico_2
    FOREIGN KEY (fk_veiculo_id_veiculo)
    REFERENCES veiculo (id_veiculo)
    ON DELETE CASCADE;
 
ALTER TABLE servico ADD CONSTRAINT FK_servico_3
    FOREIGN KEY (fk_tipo_servico_id_tiposervico)
    REFERENCES tipo_servico (id_tiposervico)
    ON DELETE CASCADE;
 
ALTER TABLE peca ADD CONSTRAINT FK_peca_2
    FOREIGN KEY (fk_fornecedor_id_fornecedor)
    REFERENCES fornecedor (id_fornecedor)
    ON DELETE CASCADE;
 
ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_2
    FOREIGN KEY (fk_servico_id_servico)
    REFERENCES servico (id_servico)
    ON DELETE CASCADE;
 
ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_3
    FOREIGN KEY (fk_tipo_pagamento_id_tipopagamento)
    REFERENCES tipo_pagamento (id_tipopagamento)
    ON DELETE RESTRICT;
 
ALTER TABLE nota_fiscal ADD CONSTRAINT FK_nota_fiscal_4
    FOREIGN KEY (fk_Faturamento_id_faturamento)
    REFERENCES Faturamento (id_faturamento)
    ON DELETE RESTRICT;
 
ALTER TABLE mecanico ADD CONSTRAINT FK_mecanico_2
    FOREIGN KEY (fk_mecanico_id_mecanico)
    REFERENCES mecanico (id_mecanico);
 
ALTER TABLE agendamento ADD CONSTRAINT FK_agendamento_2
    FOREIGN KEY (fk_veiculo_id_veiculo)
    REFERENCES veiculo (id_veiculo)
    ON DELETE CASCADE;
 
ALTER TABLE servico_peca ADD CONSTRAINT FK_servico_peca_1
    FOREIGN KEY (fk_peca_id_peca)
    REFERENCES peca (id_peca)
    ON DELETE SET NULL;
 
ALTER TABLE servico_peca ADD CONSTRAINT FK_servico_peca_2
    FOREIGN KEY (fk_servico_id_servico)
    REFERENCES servico (id_servico)
    ON DELETE SET NULL;
 
ALTER TABLE mecanico_servico ADD CONSTRAINT FK_mecanico_servico_1
    FOREIGN KEY (fk_mecanico_id_mecanico)
    REFERENCES mecanico (id_mecanico)
    ON DELETE RESTRICT;
 
ALTER TABLE mecanico_servico ADD CONSTRAINT FK_mecanico_servico_2
    FOREIGN KEY (fk_servico_id_servico)
    REFERENCES servico (id_servico)
    ON DELETE SET NULL;