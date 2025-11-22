from psycopg2 import DatabaseError

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

def listar_veiculos(conn):
    sql = "SELECT id_veiculo, marca, modelo, placa, ano, cor, fk_cliente_id_cliente FROM veiculo WHERE status = 'ATIVO' ORDER BY id_veiculo;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            veiculos = cur.fetchall()
            print("\n--- Lista de Veículos ---------------------------------------------------------------")
            print("{:<5} | {:<15} | {:<15} | {:<7} | {:<4} | {:<10} | {:<5}".format("ID", "Marca", "Modelo", "Placa", "Ano", "Cor", "ID Cliente"))
            print("-" * 85)
            for veiculo in veiculos:
                print("{:<5} | {:<15} | {:<15} | {:<7} | {:<4} | {:<10} | {:<5}".format(veiculo[0], veiculo[1], veiculo[2], veiculo[3], veiculo[4], veiculo[5], veiculo[6]))
                print("-" * 85)
    except DatabaseError as e:
        print(f" Erro ao listar veículos: {e}")

def atualizar_veiculo(conn, id_veiculo, marca=None, modelo=None, cor=None, ano=None, placa=None):
    campos = []
    valores = []
    
    if marca is not None:
        campos.append("marca = %s")
        valores.append(marca)
    if modelo is not None:
        campos.append("modelo = %s")
        valores.append(modelo)
    if cor is not None:
        campos.append("cor = %s")
        valores.append(cor)
    if ano is not None:
        campos.append("ano = %s")
        valores.append(ano)
    if placa is not None:
        campos.append("placa = %s")
        valores.append(placa.upper())
    
    if not campos:
        print(" Nenhum campo foi informado para atualização.")
        return False
    
    valores.append(id_veiculo)
    sql = f"UPDATE veiculo SET {', '.join(campos)} WHERE id_veiculo = %s AND status = 'ATIVO';"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            if cur.rowcount > 0:
                conn.commit()
                print(f" Veículo ID {id_veiculo} atualizado com sucesso!")
                return True
            else:
                print(f" Veículo ID {id_veiculo} não encontrado ou está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar veículo: {e}")
        return False

def deletar_veiculo(conn, id_veiculo):
    sql = "UPDATE veiculo SET status = 'INATIVO' WHERE id_veiculo = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_veiculo,))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Veículo ID {id_veiculo} marcado como INATIVO.")
                return True
            else:
                print(f" Veículo ID {id_veiculo} não encontrado ou já está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao deletar veículo: {e}")
        return False

def buscar_veiculo_por_id(conn, id_veiculo):
    sql = "SELECT id_veiculo, marca, modelo, placa, ano, cor FROM veiculo WHERE id_veiculo = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_veiculo,))
            return cur.fetchone()
    except DatabaseError:
        return None

