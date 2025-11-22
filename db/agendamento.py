from psycopg2 import DatabaseError

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

def listar_agendamentos(conn):
    sql = """
        SELECT id_agendamento, data, fk_veiculo_id_veiculo 
        FROM agendamento 
        WHERE status = 'ATIVO' OR status IS NULL OR status = 'ABERTO' 
        ORDER BY id_agendamento;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            agendamentos = cur.fetchall()
            
            print("\n--- Lista de Agendamentos ATIVOS ---")
            print("{:<5} | {:<20} | {:<5}".format("ID", "Data", "ID Veículo"))
            print("-" * 35)
            
            if not agendamentos:
                print("Nenhum agendamento ativo encontrado.")
                print("-" * 35)
                return []
                
            for agendamento in agendamentos:
                data_formatada = agendamento[1].strftime("%Y-%m-%d %H:%M")
                print("{:<5} | {:<20} | {:<5}".format(agendamento[0], data_formatada, agendamento[2]))
                print("-" * 35)
            
            return agendamentos
            
    except DatabaseError as e:
        print(f" Erro ao listar agendamentos: {e}")
        return []

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

def atualizar_agendamento(conn, id_agendamento, data=None):
    if data is None:
        print(" Data é obrigatória para atualização.")
        return False
    
    sql = "UPDATE agendamento SET data = %s WHERE id_agendamento = %s AND (status = 'ATIVO' OR status IS NULL OR status = 'ABERTO');"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (data, id_agendamento))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Agendamento ID {id_agendamento} atualizado com sucesso!")
                return True
            else:
                print(f" Agendamento ID {id_agendamento} não encontrado ou não pode ser atualizado.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar agendamento: {e}")
        return False

def deletar_agendamento(conn, id_agendamento):
    sql = "UPDATE agendamento SET status = 'CANCELADO' WHERE id_agendamento = %s AND (status = 'ATIVO' OR status IS NULL OR status = 'ABERTO');"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_agendamento,))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Agendamento ID {id_agendamento} marcado como CANCELADO.")
                return True
            else:
                print(f" Agendamento ID {id_agendamento} não encontrado ou não pode ser cancelado.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao deletar agendamento: {e}")
        return False

def buscar_agendamento_por_id(conn, id_agendamento):
    sql = "SELECT id_agendamento, data FROM agendamento WHERE id_agendamento = %s AND (status = 'ATIVO' OR status IS NULL OR status = 'ABERTO');"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_agendamento,))
            return cur.fetchone()
    except DatabaseError:
        return None

