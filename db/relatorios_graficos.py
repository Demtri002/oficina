from psycopg2 import DatabaseError
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def consulta1_faturamento_por_tipo_servico(conn):
    sql = """
        SELECT 
            ts.nome AS tipo_servico,
            COALESCE(SUM(isv.valor_aplicado), 0) AS faturamento_total
        FROM tipo_servico ts
        LEFT JOIN itens_servico isv ON ts.id_tiposervico = isv.fk_tipo_servico_id_tiposervico
        LEFT JOIN servico s ON isv.fk_servico_id_servico = s.id_servico
        WHERE ts.status = 'ATIVO'
            AND isv.status = 'ATIVO'
            AND (s.status IS NULL OR s.status IN ('EM_ANDAMENTO', 'FINALIZADO'))
        GROUP BY ts.id_tiposervico, ts.nome
        HAVING COALESCE(SUM(isv.valor_aplicado), 0) > 0
        ORDER BY faturamento_total DESC;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            
            if not resultados:
                print("\nNenhum dado encontrado para esta consulta.")
                return
            
            print("CONSULTA 1: FATURAMENTO POR TIPO DE SERVIÇO")
            print("="*70)
            print(f"{'Tipo de Serviço':<40} | {'Faturamento Total (R$)':<20}")
            print("-"*70)
            
            tipos = []
            valores = []
            
            for row in resultados:
                tipo, valor = row
                tipos.append(tipo)
                valores.append(float(valor))
                print(f"{tipo:<40} | R$ {valor:>15.2f}")
            
            print("-"*70)
            print(f"\nTotal de tipos de serviço: {len(resultados)}")
            
            gerar_grafico_barras(
                tipos, 
                valores, 
                "Faturamento por Tipo de Serviço",
                "Tipo de Serviço",
                "Faturamento Total (R$)",
                "consulta1_faturamento_tipo_servico.png"
            )
            
            print("\nGráfico salvo em: consulta1_faturamento_tipo_servico.png")
            
    except DatabaseError as e:
        print(f"Erro ao executar consulta 1: {e}")

def consulta2_quantidade_servicos_por_cliente(conn):
    sql = """
        SELECT 
            c.nome AS cliente,
            COUNT(DISTINCT s.id_servico) AS quantidade_servicos
        FROM cliente c
        INNER JOIN veiculo v ON c.id_cliente = v.fk_cliente_id_cliente
        INNER JOIN agendamento a ON v.id_veiculo = a.fk_veiculo_id_veiculo
        INNER JOIN servico s ON a.id_agendamento = s.fk_agendamento_id_agendamento
        WHERE c.status = 'ATIVO' 
            AND v.status = 'ATIVO'
            AND s.status IN ('EM_ANDAMENTO', 'FINALIZADO')
        GROUP BY c.id_cliente, c.nome
        HAVING COUNT(DISTINCT s.id_servico) > 0
        ORDER BY quantidade_servicos DESC;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            
            if not resultados:
                print("\nNenhum dado encontrado para esta consulta.")
                return
            
            print("\n" + "="*70)
            print("CONSULTA 2: QUANTIDADE DE SERVIÇOS POR CLIENTE")
            print("="*70)
            print(f"{'Cliente':<40} | {'Quantidade de Serviços':<20}")
            print("-"*70)
            
            clientes = []
            quantidades = []
            
            for row in resultados:
                cliente, qtd = row
                clientes.append(cliente)
                quantidades.append(int(qtd))
                print(f"{cliente:<40} | {qtd:>20}")
            
            print("-"*70)
            print(f"\nTotal de clientes com serviços: {len(resultados)}")
            
            gerar_grafico_barras(
                clientes, 
                quantidades, 
                "Quantidade de Serviços por Cliente",
                "Cliente",
                "Quantidade de Serviços",
                "consulta2_servicos_por_cliente.png"
            )
            
            print("\nGráfico salvo em: consulta2_servicos_por_cliente.png")
            
    except DatabaseError as e:
        print(f"Erro ao executar consulta 2: {e}")

def consulta3_valor_pecas_por_fornecedor(conn):
    sql = """
        SELECT 
            f.nome AS fornecedor,
            COALESCE(SUM(p.valor_unit * COALESCE(sp.quantidade, 0)), 0) AS valor_total_pecas
        FROM fornecedor f
        INNER JOIN peca p ON f.id_fornecedor = p.fk_fornecedor_id_fornecedor
        LEFT JOIN servico_peca sp ON p.id_peca = sp.fk_peca_id_peca
        LEFT JOIN servico s ON sp.fk_servico_id_servico = s.id_servico
        WHERE f.status = 'ATIVO'
            AND p.status = 'ATIVO'
            AND (s.status IS NULL OR s.status IN ('EM_ANDAMENTO', 'FINALIZADO'))
        GROUP BY f.id_fornecedor, f.nome
        HAVING COALESCE(SUM(p.valor_unit * COALESCE(sp.quantidade, 0)), 0) > 0
        ORDER BY valor_total_pecas DESC;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            resultados = cur.fetchall()
            
            if not resultados:
                print("\nNenhum dado encontrado para esta consulta.")
                return
            
            print("\n" + "="*70)
            print("CONSULTA 3: VALOR TOTAL DE PEÇAS POR FORNECEDOR")
            print("="*70)
            print(f"{'Fornecedor':<40} | {'Valor Total (R$)':<20}")
            print("-"*70)
            
            fornecedores = []
            valores = []
            
            for row in resultados:
                fornecedor, valor = row
                fornecedores.append(fornecedor)
                valores.append(float(valor))
                print(f"{fornecedor:<40} | R$ {valor:>15.2f}")
            
            print("-"*70)
            print(f"\nTotal de fornecedores com peças utilizadas: {len(resultados)}")
            
            gerar_grafico_barras(
                fornecedores, 
                valores, 
                "Valor Total de Peças por Fornecedor",
                "Fornecedor",
                "Valor Total (R$)",
                "consulta3_pecas_por_fornecedor.png"
            )
            
            print("\nGráfico salvo em: consulta3_pecas_por_fornecedor.png")
            
    except DatabaseError as e:
        print(f"Erro ao executar consulta 3: {e}")

def gerar_grafico_barras(labels, valores, titulo, label_x, label_y, nome_arquivo):
    """
    Gera um gráfico de barras e salva como arquivo PNG
    """
    try:
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(labels)), valores, color='steelblue', edgecolor='black')
        plt.xlabel(label_x, fontsize=12)
        plt.ylabel(label_y, fontsize=12)
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")

