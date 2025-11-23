import google.genai as genai
import os

client = genai.Client(api_key="AIzaSyAklcrH3qTp5bWxmmTgNF-DnWKkfnjd3qM")



def get_db_schema(conn):
    schema_str = ""
    with conn.cursor() as cursor:
        query_tables = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """
        cursor.execute(query_tables)
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            schema_str += f"Tabela: {table_name}\n"
            query_cols = """
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = %s 
                ORDER BY ordinal_position;
            """
            cursor.execute(query_cols, (table_name,))
            
            columns = cursor.fetchall()
            for col in columns:
                col_name = col[0]
                col_type = col[1]
                schema_str += f"  - {col_name} ({col_type})\n"
                
    return schema_str

def execute_sql_query_postgres(conn, query):

    if not query.strip().upper().startswith("SELECT"):
        return None, "Erro: Apenas consultas SELECT são permitidas."
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                results = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                return {"colunas": col_names, "dados": results}, None
            else:
                return {"colunas": [], "dados": []}, "Consulta executada, mas não retornou dados."
    except Exception as e:
        return None, f"Erro ao executar SQL: {e}"
    
    
def perguntar_ao_banco_com_ia(pergunta_usuario, conn):
    
    
    print(f"Pergunta do Usuário: {pergunta_usuario}")
    try:
        db_schema = get_db_schema(conn)
    except Exception as e:
        return f"Erro ao conectar ou obter schema: {e}"
    
    prompt = f"""
    Você é um assistente de banco de dados especialista em PostgreSQL.
    Sua tarefa é converter a pergunta do usuário em uma consulta SQL válida.
    O dialeto é PostgreSQL.

    Aqui está o esquema do banco de dados (schema 'public'):
    {db_schema}
    
    Pergunta do usuário:
    "{pergunta_usuario}"
    
    REGRAS OBRIGATÓRIAS:
    1. Gere *apenas* a consulta SQL. A consulta deve ser um SELECT.
    2. Não inclua nenhuma explicação, markdown (```sql) ou texto introdutório.
    3. IMPORTANTE: Ao filtrar por texto (nomes, cores, marcas, etc), use SEMPRE o operador 'ILIKE' para ignorar maiúsculas/minúsculas. 
       Exemplo: Em vez de "cor = 'prata'", use "cor ILIKE 'prata'".
    """
    
    try:
        response = client.models.generate_content(model = 'gemini-2.5-pro', contents = prompt)
        sql_query = response.text.strip().replace("```sql", "").replace("```", "")
        print(f"Query gerada:\n{sql_query}")
    except Exception as e:
        return f"Erro na API Gemini (Chamada 1): {e}"

    resultados_data, erro = execute_sql_query_postgres(conn, sql_query)
    
    if erro:
        print(f"Erro na Execução: {erro}")
        return f"Não consegui executar a consulta. O banco de dados retornou: {erro}"
    
    print(f"Resultados Brutos: {resultados_data}")

    prompt_2 = f"""
    Você é um assistente de dados amigável.
    A pergunta original do usuário foi:
    "{pergunta_usuario}"
    
    Para responder, uma consulta foi feita no banco de dados, que retornou os seguintes dados (no formato colunas e linhas):
    {resultados_data}
    
    Sua tarefa é responder à pergunta original do usuário em linguagem natural e amigável, em português.
    - Use os dados para formular sua resposta.
    - Se os dados estiverem vazios (`dados: []`), diga que não encontrou informações.
    - Não mostre os dados brutos (listas, tuplas).
    - Aja como um humano respondendo à pergunta.
    """

    try:
        response = client.models.generate_content(model = 'gemini-2.5-pro', contents = prompt_2)
        resposta_final = response.text.strip()
        return resposta_final
    except Exception as e:
        return f"Erro na API Gemini (Chamada 2): {e}"
