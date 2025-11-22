from psycopg2 import DatabaseError

def cadastrar_nota_fiscal(conn, valor_pagamento, id_servico, id_tipo_pagamento, id_faturamento):
    sql = """
        INSERT INTO nota_fiscal (valor_pagamento, fk_servico_id_servico, fk_tipo_pagamento_id_tipopagamento, fk_Faturamento_id_faturamento)
        VALUES (%s, %s, %s, %s)
        RETURNING id_notafiscal;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (valor_pagamento, id_servico, id_tipo_pagamento, id_faturamento))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Nota Fiscal gerada. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao gerar nota fiscal: {e}")
        return None

def finalizar_servico_gerar_nf(conn, id_servico):
    try:
        with conn.cursor() as cur:
            sql_consulta = """
                SELECT 
                    c.cpf,
                    SUM(COALESCE(i.valor_aplicado, 0) + 
                    COALESCE(p.valor_unit, 0)
                    ) as total_servico
                FROM servico s
                JOIN agendamento a ON s.fk_agendamento_id_agendamento = a.id_agendamento
                JOIN veiculo v ON a.fk_veiculo_id_veiculo = v.id_veiculo
                JOIN cliente c ON v.fk_cliente_id_cliente = c.id_cliente
                LEFT JOIN itens_servico i ON i.fk_servico_id_servico = s.id_servico
                LEFT JOIN servico_peca sp ON sp.fk_servico_id_servico = s.id_servico 
                LEFT JOIN peca p ON sp.fk_peca_id_peca = p.id_peca
                WHERE s.id_servico = %s
                GROUP BY c.cpf;
            """
            
            cur.execute(sql_consulta, (id_servico,))
            res = cur.fetchone()
            
            if not res:
                print(" Erro: Serviço não encontrado.")
                return False
            
            cpf_cliente, valor_total = res
            
            if valor_total is None:
                valor_total = 0.0
            
            if not cpf_cliente:
                print(" Aviso: Cliente sem CPF cadastrado.")
                cpf_cliente = None 

            sql_insert_nf = """
                INSERT INTO nota_fiscal (fk_servico_id_servico, cpf_na_nota, valor_pagamento, data_emissao)
                VALUES (%s, %s, %s, CURRENT_DATE)
                RETURNING id_notafiscal;
            """
            cur.execute(sql_insert_nf, (id_servico, cpf_cliente, valor_total))
            id_nova_nf = cur.fetchone()[0]
            conn.commit()
            
            sql_pecas_usadas = """
                SELECT 
                    p.nome_peca,
                    sp.quantidade,
                    p.valor_unit
                FROM servico_peca sp
                JOIN peca p ON sp.fk_peca_id_peca = p.id_peca
                WHERE sp.fk_servico_id_servico = %s;
            """
            cur.execute(sql_pecas_usadas, (id_servico,))
            pecas_usadas = cur.fetchall()
            
            print(f" Serviço Finalizado com Sucesso!")
            print(f" Nota Fiscal Gerada: ID {id_nova_nf}")
            print(f" CPF na Nota: {cpf_cliente}")
            print(f" Valor Total: R$ {valor_total:.2f}")
            
            if pecas_usadas:
                print("\n--- DETALHES DAS PEÇAS ---")
                for nome, qtd, valor_unit in pecas_usadas: 
                    print(f" |-> {nome}: {qtd} unidade(s) (R$ {valor_unit:.2f} / un)")
                print("--------------------------")
            else:
                print("\n--- Nenhuma peça foi utilizada neste serviço. ---")
            print("==================================")
            return True

    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao gerar Nota Fiscal: {e}")
        return False

def consultar_faturamento_por_periodo(conn, data_inicio, data_fim):
    sql = """
        SELECT 
            SUM(valor_pagamento) AS total_faturado,
            COUNT(id_notafiscal) AS total_notas
        FROM nota_fiscal
        WHERE data_emissao >= %s AND data_emissao <= %s;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (data_inicio, data_fim))
            resultado = cur.fetchone()
            
            total, num_notas = resultado
            
            if total is None:
                total = 0.00
                
            print(f"\n===  Relatório Financeiro ===")
            print(f" Período: {data_inicio} até {data_fim}")
            print(f" Quantidade de Notas Emitidas: {num_notas}")
            print(f" Faturamento Total: R$ {total:.2f}")
            print("===============================")
            
            return total
            
    except DatabaseError as e:
        print(f"Erro ao consultar faturamento: {e}")
        return None

def adicionar_nota_fiscal(conn, id_nota_fiscal, id_tipo_servico):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT valor, nome FROM tipo_servico WHERE id_tiposervico = %s", (id_tipo_servico,))
            res = cur.fetchone()
            
            if not res:
                print(" Tipo de serviço não encontrado.")
                return False
            
            valor_atual, nome_servico = res
            
            sql_insert = """
                INSERT INTO itens_nota_fiscal (fk_nota_fiscal_id, fk_tipo_servico_id_tiposervico, valor_cobrado)
                VALUES (%s, %s, %s);
            """
            
            cur.execute(sql_insert, (id_nota_fiscal, id_tipo_servico, valor_atual))
            conn.commit()
            
            print(f" Item '{nome_servico}' adicionado à NF {id_nota_fiscal} (R$ {valor_atual}).")
            return True

    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao adicionar item na nota: {e}")
        return False

def cadastrar_tipo_pagamento(conn, cnpj):
    sql = """
        INSERT INTO tipo_pagamento (cnpj)
        VALUES (%s)
        RETURNING id_tipopagamento;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (cnpj,))
            id_gerado = cur.fetchone()[0]
        conn.commit()
        print(f" Tipo de Pagamento cadastrado. ID: {id_gerado}")
        return id_gerado
    except DatabaseError as e:
        conn.rollback()
        print(f" Erro ao cadastrar tipo de pagamento: {e}")
        return None

