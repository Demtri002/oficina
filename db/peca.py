from psycopg2 import DatabaseError

def cadastrar_peca(conn, nome_peca, descricao_peca, id_fornecedor, valor_unit=None):
    sql = """
        INSERT INTO peca (nome_peca, descricao_peca, fk_fornecedor_id_fornecedor, valor_unit)
        VALUES (%s, %s, %s, %s)
        RETURNING id_peca;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nome_peca, descricao_peca, id_fornecedor, valor_unit))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        valor_msg = f" - Valor: R$ {valor_unit:.2f}" if valor_unit is not None else ""
        print(f" Peça '{nome_peca}' cadastrada. ID: {id_gerado}{valor_msg}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f"Erro ao cadastrar peça: {e}")
        return None

def listar_pecas(conn):
    sql = "SELECT id_peca, nome_peca, descricao_peca, fk_fornecedor_id_fornecedor, valor_unit FROM peca WHERE status = 'ATIVO' ORDER BY id_peca;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            pecas = cur.fetchall()
            print("\n--- Lista de Peças ---------------------------------------------------------------")
            print("{:<5} | {:<15} | {:<20} | {:<5} | {:<15}".format("ID", "Nome", "Descrição", "ID Fornecedor", "Valor Unitário"))
            print("-" * 85)
            for peca in pecas:
                valor_unit = peca[4] if peca[4] is not None else "N/A"
                if isinstance(valor_unit, (int, float)):
                    valor_unit = f"R$ {valor_unit:.2f}"
                print("{:<5} | {:<15} | {:<20} | {:<5} | {:<15}".format(
                    peca[0], peca[1] or "", peca[2] or "", peca[3] or "", valor_unit))
                print("-" * 85)
    except DatabaseError as e:
        print(f" Erro ao listar peças: {e}")

def atualizar_peca(conn, id_peca, nome_peca=None, descricao=None, id_fornecedor=None, valor_unit=None):
    campos = []
    valores = []
    
    if nome_peca is not None:
        campos.append("nome_peca = %s")
        valores.append(nome_peca)
    if descricao is not None:
        campos.append("descricao_peca = %s")
        valores.append(descricao)
    if id_fornecedor is not None:
        campos.append("fk_fornecedor_id_fornecedor = %s")
        valores.append(int(id_fornecedor))
    if valor_unit is not None:
        campos.append("valor_unit = %s")
        valores.append(float(valor_unit))
    
    if not campos:
        print(" Nenhum campo foi informado para atualização.")
        return False
    
    valores.append(id_peca)
    sql = f"UPDATE peca SET {', '.join(campos)} WHERE id_peca = %s AND status = 'ATIVO';"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            if cur.rowcount > 0:
                conn.commit()
                print(f" Peça ID {id_peca} atualizada com sucesso!")
                return True
            else:
                print(f" Peça ID {id_peca} não encontrada ou está INATIVA.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao atualizar peça: {e}")
        return False

def deletar_peca(conn, id_peca):
    sql = "UPDATE peca SET status = 'INATIVO' WHERE id_peca = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_peca,))
            if cur.rowcount > 0:
                conn.commit()
                print(f" Peça ID {id_peca} marcada como INATIVA.")
                return True
            else:
                print(f" Peça ID {id_peca} não encontrada ou já está INATIVA.")
                return False
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao deletar peça: {e}")
        return False

def buscar_peca_por_id(conn, id_peca):
    sql = "SELECT id_peca, nome_peca, descricao_peca, fk_fornecedor_id_fornecedor, valor_unit FROM peca WHERE id_peca = %s AND status = 'ATIVO';"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_peca,))
            return cur.fetchone()
    except DatabaseError:
        return None

def vincular_servico_peca(conn, id_peca, id_servico, quantidade=1):
    sql = """
        INSERT INTO servico_peca (fk_peca_id_peca, fk_servico_id_servico, quantidade)
        VALUES (%s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_peca, id_servico, quantidade))
        conn.commit()
        print(f"{quantidade} unidade(s) da peça ID {id_peca} foi vinculada ao Serviço ID {id_servico}.")
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao vincular peça ao serviço: {e}")

