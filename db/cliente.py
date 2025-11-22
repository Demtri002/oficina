from psycopg2 import DatabaseError

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

def listar_clientes(conn):
    sql = "SELECT id_cliente, nome, telefone, email, cpf, endereco FROM cliente WHERE status = 'ATIVO' ORDER BY id_cliente;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            clientes = cur.fetchall()
            print("\n--- Lista de Clientes --------------------------------------------------------------------------------------------------")
            print("{:<5} | {:<30} | {:<11} | {:<30} | {:<11} | {:<30}".format("ID", "Nome", "Telefone", "Email", "CPF", "Endereço"))
            print("-" * 120)
            for cliente in clientes:
                print("{:<5} | {:<30} | {:<11} | {:<30} | {:<11} | {:<30}".format(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5]))
                print("-" * 120)
    except DatabaseError as e:
        print(f" Erro ao listar clientes: {e}")

def atualizar_cliente(conn, id_cliente, nome=None, telefone=None, email=None, cpf=None, endereco=None):
    campos = []
    valores = []
    
    if nome is not None:
        campos.append("nome = %s")
        valores.append(nome)
    if telefone is not None:
        campos.append("telefone = %s")
        valores.append(telefone)
    if email is not None:
        campos.append("email = %s")
        valores.append(email)
    if cpf is not None:
        campos.append("cpf = %s")
        valores.append(cpf)
    if endereco is not None:
        campos.append("endereco = %s")
        valores.append(endereco)
    
    if not campos:
        print(" Nenhum campo foi informado para atualização.")
        return False
    
    valores.append(id_cliente)
    sql = f"UPDATE cliente SET {', '.join(campos)} WHERE id_cliente = %s AND status = 'ATIVO';"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            if cur.rowcount > 0:
                conn.commit()
                print(f" Cliente ID {id_cliente} atualizado com sucesso!")
                return True
            else:
                print(f" Cliente ID {id_cliente} não encontrado ou está INATIVO.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar cliente: {e}")
        return False

def deletar_cliente(conn, id_cliente):
    sql_cliente = "UPDATE cliente SET status = 'INATIVO' WHERE id_cliente = %s AND status = 'ATIVO';"
    sql_propagar_veiculos = "UPDATE veiculo SET status = 'INATIVO' WHERE fk_cliente_id_cliente = %s AND status = 'ATIVO';"

    try:
        with conn.cursor() as cur:
            cur.execute(sql_cliente, (id_cliente,))
            if cur.rowcount > 0:
                cur.execute(sql_propagar_veiculos, (id_cliente,))
                num_veiculos_afetados = cur.rowcount
        
                conn.commit()
                
                print(f"Cliente ID {id_cliente} DELETADO.")
                print(f"{num_veiculos_afetados} veículo(s) relacionado(s) também foram DELETADOS.")
                return True
            else:
                print(f" Cliente ID {id_cliente} não encontrado ou já foi DELETADO.")
                return False
                
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao deletar cliente e propagar: {e}")
        return False

def buscar_cliente_por_id(conn, id_cliente):
    sql = "SELECT id_cliente, nome, telefone, email, cpf, endereco FROM cliente WHERE id_cliente = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_cliente,))
            return cur.fetchone()
    except DatabaseError:
        return None

