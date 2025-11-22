from psycopg2 import DatabaseError

def cadastrar_servico(conn, nome, descricao, custo, id_veiculo, id_tipo_servico):
    sql = """
        INSERT INTO servico (nome, descricao, fk_veiculo_id_veiculo, fk_tipo_servico_id_tiposervico)
        VALUES (%s, %s, %s, %s)
        RETURNING id_servico;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, descricao, custo, id_veiculo, id_tipo_servico))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Serviço '{nome}' criado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar serviço: {e}")
        return None

def abrir_ordem_servico(conn, id_agendamento, descricao):
    sql = """
        INSERT INTO servico (fk_agendamento_id_agendamento, descricao)
        VALUES (%s, %s)
        RETURNING id_servico;
    """
    
    sql_update_agendamento = """
        UPDATE agendamento 
        SET status = 'CANCELADO' 
        WHERE id_agendamento = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_agendamento, descricao))
            id_gerado = cur.fetchone()[0]
            cur.execute(sql_update_agendamento, (id_agendamento,))
            conn.commit()
            print(f" Ordem de Serviço #{id_gerado} aberta!")
            return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao abrir serviço: {e}")
        return None

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
        print(f"Erro ao iniciar serviço: {e}")
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

