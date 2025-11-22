from psycopg2 import DatabaseError

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

def atualizar_tipo_servico(conn, id_tiposervico, nome=None, descricao=None, valor=None):
    campos = []
    valores = []
    
    if nome is not None:
        campos.append("nome = %s")
        valores.append(nome)
    if descricao is not None:
        campos.append("descricao = %s")
        valores.append(descricao)
    if valor is not None:
        campos.append("valor = %s")
        valores.append(float(valor))
    
    if not campos:
        print(" Nenhum campo foi informado para atualização.")
        return False
    
    valores.append(id_tiposervico)
    sql = f"UPDATE tipo_servico SET {', '.join(campos)} WHERE id_tiposervico = %s AND status = 'ATIVO';"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            if cur.rowcount > 0:
                conn.commit()
                print(f" Tipo de Serviço ID {id_tiposervico} atualizado com sucesso!")
                return True
            else:
                print(f" Tipo de Serviço ID {id_tiposervico} não encontrado ou está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar tipo de serviço: {e}")
        return False

def buscar_tipo_servico_por_id(conn, id_tiposervico):
    sql = "SELECT id_tiposervico, nome, descricao, valor FROM tipo_servico WHERE id_tiposervico = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_tiposervico,))
            return cur.fetchone()
    except DatabaseError:
        return None

