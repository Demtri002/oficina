from database import *
from ai_integration import perguntar_ao_banco_com_ia


def executar_setup_inicial(conn):
    print("--- ATENÇÃO: MODO ADMIN ---")
    print("Esta operação apagará TODAS as tabelas e dados existentes.")
    confirm = input("Tem certeza que deseja zerar o banco? (s/n): ")
    
    if confirm.lower() == 's':
        eliminar_tabelas(conn)
        criar_tabelas(conn)
        
        popular = input("Deseja popular o banco com dados de teste? (s/n): ")
        if popular.lower() == 's':
            inserir_dados_iniciais(conn) 
            
        print("--- Banco de dados recriado com sucesso! ---")
    else:
        print("Operação cancelada.")

def menu_cadastros(conn):
    while True:
        print("\n--- Menu de Cadastros ---")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Veículo")
        print("3. Cadastrar Agendamento")
        print("4. Cadastrar Mecânico")        
        print("5. Cadastrar Tipos de Serviço")
        print("6. Cadastrar Peça")
        print("7. Cadastrar Fornecedor")
        print("8. Abrir Ordem de Serviço para Agendamento")
        print("9. Finalizar Serviço e Emitir Nota Fiscal")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            print("\n--- Novo Cliente ---")
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")
            
            if nome:
                cadastrar_cliente(conn, nome, telefone, email, cpf, endereco)
            else:
                print("Nome é obrigatório.")
        
        elif escolha == '2':
            print("\n--- Novo Veículo ---")
    
            cpf_cliente = input("Digite o CPF do proprietário: ") 
            placa = input("Placa (7 caracteres): ").upper()
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            cor = input("Cor: ")
    
            try:
                ano = int(input("Ano: "))
        
                if placa and marca and modelo and cpf_cliente:
                    cadastrar_veiculo(conn, marca, cor, ano, modelo, placa, cpf_cliente)
                else:
                    print("Todos os dados são obrigatórios.")
            except ValueError:
                print("Erro: O Ano deve ser numérico.")
        
        elif escolha == '3':
            print("\n--- Novo Agendamento ---")
            listar_veiculos(conn) 

            placa = input("Digite a Placa do Veículo: ").upper()
            data = input("Data e Hora (AAAA-MM-DD HH:MM:SS): ")
    
            if placa and data:
                cadastrar_agendamento(conn, data, placa)
            else:
                print("Placa e Data são obrigatórios.")
            
        elif escolha == '4':
            print("\n--- Novo Mecânico ---")
            nome = input("Nome: ")
            cargo = input("Cargo: ")
            email = input("Email: ")
            
            tem_supervisor = input("Tem supervisor? (s/n): ").lower()
            id_supervisor = None
            if tem_supervisor == 's':
                id_supervisor = input("ID do Supervisor: ")
            
            if nome and cargo:
                cadastrar_mecanico(conn, nome, cargo, email, id_supervisor)
            else:
                print("Nome e Cargo são obrigatórios.")

        elif escolha == '5':
            print("\n--- Novo Tipo de Serviço ---") 
            nome = input("Nome do Serviço: ") 
            descricao = input("Descrição: ")
            try:
                valor = float(input("Valor (R$): "))
                if nome:
                    cadastrar_tipo_servico(conn, nome, descricao, valor)
                else:
                    print("Nome é obrigatório.")
            except ValueError:
                print("Erro: O valor deve ser numérico.")

        elif escolha == '6':
             print("\n--- Nova Peça ---")
             nome_peca = input("Nome da Peça: ")
             descricao = input("Descrição: ")
             try:
                 id_fornecedor = int(input("ID do Fornecedor: "))
                 valor_input = input("Valor Unitário (R$) - opcional, pressione Enter para pular: ").strip()
                 valor_unit = float(valor_input) if valor_input else None
                 cadastrar_peca(conn, nome_peca, descricao, id_fornecedor, valor_unit)
             except ValueError:
                 print("Erro: ID do fornecedor ou valor inválido.")

        elif escolha == '7':
            print("\n--- Novo Fornecedor ---")
            nome = input("Nome do Fornecedor: ")
            if nome:
                cadastrar_fornecedor(conn, nome)

        elif escolha == '8': 
            print("\n---  Execução de Serviço ---")
            
            try:
                id_agendamento = int(input("Digite o ID do Agendamento: "))
            
                dados = buscar_agendamento_detalhado(conn, id_agendamento)
            
                if dados:
                    data, modelo, placa, cliente = dados
                    print("\n Detalhes do Agendamento:")
                    print(f" Cliente: {cliente}")
                    print(f" Veículo: {modelo} ({placa})")
                    print(f" Data Agendada: {data}")
            
                    confirmar = input("\nConfirma abrir serviço para este agendamento? (s/n): ")
                    if confirmar.lower() == 's':
                        desc = input("Observação do serviço: ")
                    
                        id_servico = abrir_ordem_servico(conn, id_agendamento, desc)
                    
                        if id_servico:
                            
                            iniciar_servico(conn, id_servico)
                            
                            while True:
                                listar_servicos_simples(conn) 
                                print("\nAdicionar tipo de serviço à ordem?")
                                op_item = input("Digite o ID do Tipo (ou '0' para encerrar a execução): ")
                            
                                if op_item == '0':
                                    break
                                
                                try:
                                    adicionar_item_servico(conn, id_servico, int(op_item))
                                except ValueError:
                                    print("ID inválido.")
                            
                            total = calcular_valor_total_servico(conn, id_servico)
                            print(f"\n Execução de Serviço Concluída! Total parcial: R$ {total:.2f}")
                            print(" O serviço está agora em 'EM_ANDAMENTO'. Use a Opção 9 para Faturar e Finalizar.")
                        else:
                            print("Não foi possível abrir a Ordem de Serviço.")
                    else:
                        print("Operação cancelada.")
                else:
                    print("Agendamento não encontrado.")
            
            except ValueError:
                print("Erro: O ID deve ser um número.")
        

        elif escolha == '9':
            print("\n--- Finalizar Serviço e Emitir Nota Fiscal ---")
            
            listar_servicos_em_andamento(conn)
            
            id_servico = input("Digite o ID do Serviço (EM_ANDAMENTO) a ser finalizado: ")
            
            if not id_servico.isdigit():
                print(" ID do Serviço inválido.")
                continue

            id_servico = int(id_servico)
            
            try:
                with conn.cursor() as cur:
                    sql_update_status = "UPDATE servico SET status = 'FINALIZADO' WHERE id_servico = %s AND status = 'EM_ANDAMENTO'"
                    cur.execute(sql_update_status, (id_servico,))
                    
                    if cur.rowcount == 0:
                        print(f" Serviço {id_servico} não encontrado ou não está em 'EM_ANDAMENTO'.")
                        conn.rollback()
                        continue
                        
                    conn.commit()
                    print(f" Status do Serviço {id_servico} alterado para 'FINALIZADO'.")

                finalizar_servico_gerar_nf(conn, id_servico)
                
            except DatabaseError as e:
                conn.rollback()
                print(f" Erro na transação de finalização/faturamento: {e}")

        elif escolha == '0':
            break 
        else:
            print("Escolha inválida.")
        
    
def menu_relatorios(conn):
    while True:
        print("\n--- Menu de Relatórios ---")
        print("1. Consultar Clientes")
        print("2. Consultar Veículos")
        print("3. Consultar Agendamentos")
        print("4. Consultar Serviços em Andamento")
        print("5. Consultar Serviços Finalizados")
        print("6. Consultar Faturamento por Período")
        print("7. Consultar com IA (Gemini)")
        print("8. Consultar Mecânicos")
        print("9. Consultar Fornecedores")
        print("10. Consulta Sumarizada 1: Faturamento por Tipo de Serviço (com gráfico)")
        print("11. Consulta Sumarizada 2: Quantidade de Serviços por Cliente (com gráfico)")
        print("12. Consulta Sumarizada 3: Valor de Peças por Fornecedor (com gráfico)")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            listar_clientes(conn)
        elif escolha == '2':
            listar_veiculos(conn)
        elif escolha == '3':
            listar_agendamentos(conn)
        elif escolha == '4':
            listar_servicos_em_andamento(conn)
        elif escolha == '5':
            listar_servicos_finalizados(conn)
        elif escolha == '6':
            print("\n---  Consulta de Faturamento por Período ---")
            data_inicio = input("Data Inicial (AAAA-MM-DD): ")
            data_fim = input("Data Final (AAAA-MM-DD): ")
    
            if len(data_inicio) == 10 and len(data_fim) == 10:
                data_fim_ajustada = f"{data_fim} 23:59:59" 
                
                consultar_faturamento_por_periodo(conn, data_inicio, data_fim_ajustada)
            else:
                print(" Formato de data inválido ou campos vazios. Use AAAA-MM-DD.")

        elif escolha == '7':
            print("\n--- Assistente Virtual ---")
            print("Ex: 'Liste todos os clientes', 'Quantos veículos temos?', 'Mostre os agendamentos'")
            prompt = input("Faça sua pergunta ao banco: ")
            resposta = perguntar_ao_banco_com_ia(prompt, conn)
            print(f"{resposta}")
        elif escolha == '8':
            listar_mecanicos(conn)
        elif escolha == '9':
            listar_fornecedores(conn)
        elif escolha == '10':
            consulta1_faturamento_por_tipo_servico(conn)
        elif escolha == '11':
            consulta2_quantidade_servicos_por_cliente(conn)
        elif escolha == '12':
            consulta3_valor_pecas_por_fornecedor(conn)
        elif escolha == '0':
            break
        else:
            print("Escolha inválida.")

def menu_atualizacoes(conn):
    while True:
        print("\n--- Menu de Atualizações ---")
        print("1. Atualizar Cliente")
        print("2. Atualizar Veículo")
        print("3. Atualizar Agendamento")
        print("4. Atualizar Mecânico")
        print("5. Atualizar Fornecedor")
        print("6. Atualizar Tipo de Serviço")
        print("7. Atualizar Peça")
        print("8. Adicionar Peça a um Serviço")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            print("\n--- Atualizar Cliente ---")
            listar_clientes(conn)
            try:
                id_cliente = int(input("Digite o ID do Cliente a ser atualizado: "))
                cliente = buscar_cliente_por_id(conn, id_cliente)
                
                if not cliente:
                    print(f" Cliente ID {id_cliente} não encontrado ou está INATIVO.")
                    continue
                
                print(f"\n Dados atuais do Cliente ID {id_cliente}:")
                print(f" Nome: {cliente[1]}")
                print(f" Telefone: {cliente[2]}")
                print(f" Email: {cliente[3]}")
                print(f" CPF: {cliente[4]}")
                print(f" Endereço: {cliente[5]}")
                print("\n Deixe em branco para manter o valor atual.")
                
                nome = input("Novo Nome (ou Enter para manter): ").strip() or None
                telefone = input("Novo Telefone (ou Enter para manter): ").strip() or None
                email = input("Novo Email (ou Enter para manter): ").strip() or None
                cpf = input("Novo CPF (ou Enter para manter): ").strip() or None
                endereco = input("Novo Endereço (ou Enter para manter): ").strip() or None
                
                atualizar_cliente(conn, id_cliente, nome, telefone, email, cpf, endereco)
            except ValueError:
                print(" Erro: ID deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
                
        elif escolha == '2':
            print("\n--- Atualizar Veículo ---")
            listar_veiculos(conn)
            try:
                id_veiculo = int(input("Digite o ID do Veículo a ser atualizado: "))
                veiculo = buscar_veiculo_por_id(conn, id_veiculo)
                
                if not veiculo:
                    print(f" Veículo ID {id_veiculo} não encontrado ou está INATIVO.")
                    continue
                
                print(f"\n Dados atuais do Veículo ID {id_veiculo}:")
                print(f" Marca: {veiculo[1]}")
                print(f" Modelo: {veiculo[2]}")
                print(f" Placa: {veiculo[3]}")
                print(f" Ano: {veiculo[4]}")
                print(f" Cor: {veiculo[5]}")
                print("\n Deixe em branco para manter o valor atual.")
                
                marca = input("Nova Marca (ou Enter para manter): ").strip() or None
                modelo = input("Novo Modelo (ou Enter para manter): ").strip() or None
                placa = input("Nova Placa (ou Enter para manter): ").strip() or None
                cor = input("Nova Cor (ou Enter para manter): ").strip() or None
                ano_input = input("Novo Ano (ou Enter para manter): ").strip()
                ano = int(ano_input) if ano_input else None
                
                atualizar_veiculo(conn, id_veiculo, marca, modelo, cor, ano, placa)
            except ValueError:
                print(" Erro: ID ou Ano deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
                
        elif escolha == '3':
            print("\n--- Atualizar Agendamento ---")
            listar_agendamentos(conn)
            try:
                id_agendamento = int(input("Digite o ID do Agendamento a ser atualizado: "))
                agendamento = buscar_agendamento_por_id(conn, id_agendamento)
                
                if not agendamento:
                    print(f" Agendamento ID {id_agendamento} não encontrado ou não pode ser atualizado.")
                    continue
                
                print(f"\n Dados atuais do Agendamento ID {id_agendamento}:")
                print(f" Data: {agendamento[1]}")
                
                data = input("Nova Data e Hora (AAAA-MM-DD HH:MM:SS) (ou Enter para manter): ").strip()
                if not data:
                    print(" Nenhuma alteração realizada.")
                    continue
                
                atualizar_agendamento(conn, id_agendamento, data)
            except ValueError:
                print(" Erro: ID deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
                
        elif escolha == '4':
            print("\n--- Atualizar Mecânico ---")
            listar_mecanicos(conn)
            try:
                id_mecanico = int(input("Digite o ID do Mecânico a ser atualizado: "))
                mecanico = buscar_mecanico_por_id(conn, id_mecanico)
                
                if not mecanico:
                    print(f" Mecânico ID {id_mecanico} não encontrado ou está INATIVO.")
                    continue
                
                print(f"\n Dados atuais do Mecânico ID {id_mecanico}:")
                print(f" Nome: {mecanico[1]}")
                print(f" Cargo: {mecanico[2]}")
                print(f" Email: {mecanico[3]}")
                print(f" ID Supervisor: {mecanico[4]}")
                print("\n Deixe em branco para manter o valor atual.")
                
                nome = input("Novo Nome (ou Enter para manter): ").strip() or None
                cargo = input("Novo Cargo (ou Enter para manter): ").strip() or None
                email = input("Novo Email (ou Enter para manter): ").strip() or None
                id_supervisor = input("Novo ID Supervisor (ou Enter para manter, '0' para remover): ").strip()
                if id_supervisor == '':
                    id_supervisor = None
                elif id_supervisor == '0':
                    id_supervisor = ''
                else:
                    id_supervisor = int(id_supervisor)
                
                atualizar_mecanico(conn, id_mecanico, nome, cargo, email, id_supervisor)
            except ValueError:
                print(" Erro: ID deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
                
        elif escolha == '5':
            print("\n--- Atualizar Fornecedor ---")
            listar_fornecedores(conn)
            try:
                id_fornecedor = int(input("Digite o ID do Fornecedor a ser atualizado: "))
                fornecedor = buscar_fornecedor_por_id(conn, id_fornecedor)
                
                if not fornecedor:
                    print(f" Fornecedor ID {id_fornecedor} não encontrado ou está INATIVO.")
                    continue
                
                print(f"\n Dados atuais do Fornecedor ID {id_fornecedor}:")
                print(f" Nome: {fornecedor[1]}")
                
                nome = input("Novo Nome: ").strip()
                if not nome:
                    print(" Nome é obrigatório.")
                    continue
                
                atualizar_fornecedor(conn, id_fornecedor, nome)
            except ValueError:
                print(" Erro: ID deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
                
        elif escolha == '6':
            print("\n--- Atualizar Tipo de Serviço ---")
            listar_servicos_simples(conn)
            try:
                id_tiposervico = int(input("Digite o ID do Tipo de Serviço a ser atualizado: "))
                tipo_servico = buscar_tipo_servico_por_id(conn, id_tiposervico)
                
                if not tipo_servico:
                    print(f" Tipo de Serviço ID {id_tiposervico} não encontrado ou está INATIVO.")
                    continue
                
                print(f"\n Dados atuais do Tipo de Serviço ID {id_tiposervico}:")
                print(f" Nome: {tipo_servico[1]}")
                print(f" Descrição: {tipo_servico[2]}")
                print(f" Valor: R$ {tipo_servico[3]:.2f}")
                print("\n Deixe em branco para manter o valor atual.")
                
                nome = input("Novo Nome (ou Enter para manter): ").strip() or None
                descricao = input("Nova Descrição (ou Enter para manter): ").strip() or None
                valor_input = input("Novo Valor (ou Enter para manter): ").strip()
                valor = float(valor_input) if valor_input else None
                
                atualizar_tipo_servico(conn, id_tiposervico, nome, descricao, valor)
            except ValueError:
                print(" Erro: ID ou Valor deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
                
        elif escolha == '7':
            print("\n--- Atualizar Peça ---")
            listar_pecas(conn)
            try:
                id_peca = int(input("Digite o ID da Peça a ser atualizada: "))
                peca = buscar_peca_por_id(conn, id_peca)
                
                if not peca:
                    print(f" Peça ID {id_peca} não encontrada ou está INATIVA.")
                    continue
                
                print(f"\n Dados atuais da Peça ID {id_peca}:")
                print(f" Nome: {peca[1]}")
                print(f" Descrição: {peca[2]}")
                print(f" ID Fornecedor: {peca[3]}")
                valor_display = f"R$ {peca[4]:.2f}" if peca[4] is not None else "N/A"
                print(f" Valor Unitário: {valor_display}")
                print("\n Deixe em branco para manter o valor atual.")
                
                nome_peca = input("Novo Nome (ou Enter para manter): ").strip() or None
                descricao = input("Nova Descrição (ou Enter para manter): ").strip() or None
                id_fornecedor_input = input("Novo ID Fornecedor (ou Enter para manter): ").strip()
                id_fornecedor = int(id_fornecedor_input) if id_fornecedor_input else None
                valor_input = input("Novo Valor Unitário (ou Enter para manter): ").strip()
                valor_unit = float(valor_input) if valor_input else None
                
                atualizar_peca(conn, id_peca, nome_peca, descricao, id_fornecedor, valor_unit)
            except ValueError:
                print(" Erro: ID ou Valor deve ser um número.")
            except Exception as e:
                print(f" Erro: {e}")
        elif escolha == '8':
            print("\n--- Adicionar Peça a um Serviço ---")
            listar_servicos_em_andamento(conn)
            try:
                id_servico = int(input("Digite o ID do Serviço (EM_ANDAMENTO): "))
                listar_pecas(conn)
                id_peca = int(input("Digite o ID da Peça a ser adicionada: "))
                quantidade_input = input("Quantidade (padrão 1): ").strip()
                quantidade = int(quantidade_input) if quantidade_input else 1
                
                if quantidade <= 0:
                    print(" Quantidade deve ser maior que zero.")
                    continue
                adicionar_peca_servico(conn, id_servico, id_peca, quantidade)
            except ValueError:
                print(" Erro: IDs ou Quantidade devem ser números.")
            except Exception as e:
                print(f" Erro: {e}")        
        elif escolha == '0':
            break
        else:
            print("Escolha inválida.")
    
def menu_delecoes(conn):
    while True:
        print("\n--- Menu de Deleções ---")
        print("1. Deletar Clientes")
        print("2. Deletar Veículos")
        print("3. Deletar Agendamentos")
        print("4. Deletar Mecânicos")
        print("5. Deletar Fornecedores")
        print("0. Voltar ao Menu Principal")
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            listar_clientes(conn)
            id_cliente = input("Digite o ID do Cliente a ser deletado: ")
            confirmar = input(f"Tem certeza que deseja deletar o cliente {id_cliente}? (s/n): ")
            if confirmar.lower() == 's':
                deletar_cliente(conn, id_cliente)
        elif escolha == '2':
            listar_veiculos(conn)
            id_veiculo = input("Digite o ID do Veículo a ser deletado: ")
            confirmar = input(f"Tem certeza que deseja deletar o veículo {id_veiculo}? (s/n): ")
            if confirmar.lower() == 's':
                deletar_veiculo(conn, id_veiculo)
        elif escolha == '3':
            listar_agendamentos(conn)
            id_agendamento = input("Digite o ID do Agendamento a ser deletado: ") 
            confirmar = input(f"Tem certeza que deseja deletar o agendamento {id_agendamento}? (s/n): ")
            if confirmar.lower() == 's':
                deletar_agendamento(conn, id_agendamento)
        elif escolha == '4':
            listar_mecanicos(conn)
            id_mecanico = input("Digite o ID do Mecânico a ser deletado: ")
            confirmar = input(f"Tem certeza que deseja deletar o mecânico {id_mecanico}? (s/n): ")
            if confirmar.lower() == 's':
                deletar_mecanico(conn, id_mecanico)
        elif escolha == '5':
            listar_fornecedores(conn)
            id_fornecedor = input("Digite o ID do Fornecedor a ser deletado: ")
            confirmar = input(f"Tem certeza que deseja deletar o fornecedor {id_fornecedor}? (s/n): ")
            if confirmar.lower() == 's':
                deletar_fornecedor(conn, id_fornecedor)
        elif escolha == '0':
            break
        else:
            print("Escolha inválida.")
            
if __name__ == "__main__":
    conn = None
    try:
        conn = conecta()
        if conn:
            criar_tabelas(conn) 
            
            if True:
                print("Login bem-sucedido.")
                while True:
                    print("\n--- MENU PRINCIPAL ---")
                    print("1. Cadastros")
                    print("2. Relatórios / Consultas")
                    print("3. Atualizar Cadastros")
                    print("4. Deletar Cadastros")
                    print("------------------------")
                    print("9. [Admin] Reiniciar Banco de Dados (APAGA TUDO)")
                    print("0. Sair do Sistema")
                    
                    escolha_main = input("Escolha uma opção: ")

                    if escolha_main == '1':
                        menu_cadastros(conn)
                    elif escolha_main == '2':
                        menu_relatorios(conn)
                    elif escolha_main == '3':
                        menu_atualizacoes(conn)
                    elif escolha_main == '4':
                        menu_delecoes(conn)
                    elif escolha_main == '9':
                        executar_setup_inicial(conn)
                    elif escolha_main == '0':
                        print("Saindo do sistema...")
                        break 
                    else:
                        print("Opção inválida.")
        else:
            print("Não foi possível conectar ao banco de dados.")
            print("Verifique se o PostgreSQL está rodando e as credenciais no database.py.")
            
    except Exception as e:
        print(f"Ocorreu um erro crítico no programa: {e}")
    finally:
        if conn:
            encerra_conexao(conn)