
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