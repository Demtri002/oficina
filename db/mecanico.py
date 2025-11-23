from psycopg2 import DatabaseError

def login_mecanico(conn, email, senha):
    sql = """
        SELECT id_mecanico, nome, cargo 
        FROM mecanico 
        WHERE email = %s AND senha = %s
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (email, senha))
            resultado = cur.fetchone()

            if resultado:
                return {
                    "id": resultado[0],
                    "nome": resultado[1],
                    "cargo": resultado[2]
                }
            else:
                return None
    except Exception as e:
        print(f"Erro na autenticação: {e}")
        return None

def cadastrar_mecanico(conn, nome, cargo, email, senha, id_supervisor=None):
    sql = """
        INSERT INTO mecanico (nome, cargo, email, senha, fk_mecanico_id_mecanico)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_mecanico;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cargo, email, senha, id_supervisor))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Mecânico '{nome}' cadastrado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar mecânico: {e}")
        return None

def listar_mecanicos(conn):
    sql = "SELECT id_mecanico, nome, cargo, email, fk_mecanico_id_mecanico FROM mecanico WHERE status = 'ATIVO' ORDER BY id_mecanico;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            mecanicos = cur.fetchall()
            print("\n--- Lista de Mecânicos ---")
            print("{:<5} | {:<25} | {:<30} | {:<40} | {:<5}".format("ID", "Nome", "Cargo", "Email", "ID Supervisor"))
            print("-" * 110)
            for mecanico in mecanicos:
                id_supervisor = mecanico[4]
                id_supervisor_formatado = id_supervisor if id_supervisor is not None else ""
                print("{:<5} | {:<25} | {:<30} | {:<40} | {:<5}".format(mecanico[0], mecanico[1], mecanico[2], mecanico[3], id_supervisor_formatado))
                print("-" * 110)
    except DatabaseError as e:
        print(f" Erro ao listar mecânicos: {e}")

def atualizar_mecanico(conn, id_mecanico, nome=None, cargo=None, email=None, senha=None, id_supervisor=None):
    campos = []
    valores = []
    
    if nome is not None:
        campos.append("nome = %s")
        valores.append(nome)
    if cargo is not None:
        campos.append("cargo = %s")
        valores.append(cargo)
    if email is not None:
        campos.append("email = %s")
        valores.append(email)
    if senha is not None:
        campos.append("senha = %s")
        valores.append(senha)
    if id_supervisor is not None:
        if id_supervisor == '':
            campos.append("fk_mecanico_id_mecanico = NULL")
        else:
            campos.append("fk_mecanico_id_mecanico = %s")
            valores.append(int(id_supervisor))
    
    if not campos:
        print(" Nenhum campo foi informado para atualização.")
        return False
    
    valores.append(id_mecanico)
    sql = f"UPDATE mecanico SET {', '.join(campos)} WHERE id_mecanico = %s AND status = 'ATIVO';"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            if cur.rowcount > 0:
                conn.commit()
                print(f" Mecânico ID {id_mecanico} atualizado com sucesso!")
                return True
            else:
                print(f" Mecânico ID {id_mecanico} não encontrado ou está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar mecânico: {e}")
        return False

def deletar_mecanico(conn, id_mecanico):
    sql = "UPDATE mecanico SET status = 'INATIVO' WHERE id_mecanico = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_mecanico,))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Mecânico ID {id_mecanico} marcado como INATIVO.")
                return True
            else:
                print(f" Mecânico ID {id_mecanico} não encontrado ou já está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao deletar mecânico: {e}")
        return False

def buscar_mecanico_por_id(conn, id_mecanico):
    sql = "SELECT id_mecanico, nome, cargo, email, fk_mecanico_id_mecanico FROM mecanico WHERE id_mecanico = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_mecanico,))
            return cur.fetchone()
    except DatabaseError:
        return None

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

