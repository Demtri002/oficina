from psycopg2 import DatabaseError

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

def listar_fornecedores(conn):
    sql = "SELECT id_fornecedor, nome FROM fornecedor WHERE status = 'ATIVO' ORDER BY id_fornecedor;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            fornecedores = cur.fetchall()
            print("\n--- Lista de Fornecedores ---")
            print("{:<5} | {:<30} ".format("ID", "Nome"))
            print("-" * 40)
            for fornecedor in fornecedores:
                print("{:<5} | {:<30} ".format(fornecedor[0], fornecedor[1]))
                print("-" * 40)
    except DatabaseError as e:
        print(f" Erro ao listar fornecedores: {e}")

def atualizar_fornecedor(conn, id_fornecedor, nome=None):
    if nome is None:
        print(" Nome é obrigatório para atualização.")
        return False
    
    sql = "UPDATE fornecedor SET nome = %s WHERE id_fornecedor = %s AND status = 'ATIVO';"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, id_fornecedor))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Fornecedor ID {id_fornecedor} atualizado com sucesso!")
                return True
            else:
                print(f" Fornecedor ID {id_fornecedor} não encontrado ou está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar fornecedor: {e}")
        return False

def deletar_fornecedor(conn, id_fornecedor):
    sql = "UPDATE fornecedor SET status = 'INATIVO' WHERE id_fornecedor = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_fornecedor,))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Fornecedor ID {id_fornecedor} marcado como INATIVO.")
                return True
            else:
                print(f" Fornecedor ID {id_fornecedor} não encontrado ou já está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao deletar fornecedor: {e}")
        return False

def buscar_fornecedor_por_id(conn, id_fornecedor):
    sql = "SELECT id_fornecedor, nome FROM fornecedor WHERE id_fornecedor = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_fornecedor,))
            return cur.fetchone()
    except DatabaseError:
        return None

