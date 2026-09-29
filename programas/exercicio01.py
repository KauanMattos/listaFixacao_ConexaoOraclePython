import oracledb as orcl
import pandas as pd
import os
from dotenv import load_dotenv

def main():
    conexao_BD, inst_SQL, conexao = conectar_BD()

    if (conexao_BD):
        opcao = 1
        while opcao != 7:
            # Os relatórios dos itens 5 e 6 devem ser convertidos em arquivo texto
            print("1 - Inserir um registro")
            print("2 - Alterar um registro")
            print("3 - Excluir um registro")
            print("4 - Relatório de todos os registros")
            print("5 - Relatório dos funcionários com salários entre 8k a 12k")
            print("6 - Relatório dos funcionários com cargo Desenvolvedor front-end com idade acima de 26 anos")
            print("7 - Sair")

            try:
                opcao = int(input("Digite a opção desejada: (1 a 7): "))
            except ValueError:
                print("Por favor, digite um número válido de 1 a 7.")
                continue
            if 1 <= opcao <= 7:
                match opcao:
                    case 1:
                        inserir_funcionario(inst_SQL, conexao)
                    case 2:
                        alterar_funcionario(inst_SQL, conexao)
                    case 3:
                        excluir_funcionario(inst_SQL, conexao)
                    case 4:
                        exibir_funcionarios(inst_SQL)
                    case 5:
                        relatorio_salario(inst_SQL)
                    case 6:
                        relatorio_cargo_idade(inst_SQL)
                    case 7:
                        print("Saindo do programa...")
                        conexao.close()
            else:
                print("Opção Inválida")

def conectar_BD():

    # Carregando as variáveis do arquivo .env para o ambiente
    load_dotenv()

    try:
        # Pega os valores ocultos do arquivo .env
        host = os.getenv("ORACLE_HOST")
        port = os.getenv("ORACLE_PORT")
        service = os.getenv("ORACLE_SERVICE")
        user = os.getenv("ORACLE_USER")
        password = os.getenv("ORACLE_PASSWORD")

        # String de conexao com o servidor do BD
        str_conexao = orcl.makedsn(host, port, service)
        # Configurar a conexao com BD usando as credenciais ocultas
        conexao = orcl.connect(user=user, password=password, dsn=str_conexao)

        inst_SQL = conexao.cursor()
    except Exception as erro:
        print(f"Erro: {erro}")
        conexao_BD = False
    else:
        conexao_BD = True

    return (conexao_BD, inst_SQL, conexao)

def inserir_funcionario(inst_SQL, conexao):
    try:
        funcionario_cpf = int(input("Digite o CPF do funcionário: "))
        funcionario_nome = (input("Digite o nome do funcionário: "))
        funcionario_cargo = (input("Digite o cargo do funcionário: "))
        funcionario_salario = (float(input("Digite o salário do funcionário: ")))
        funcionario_idade = int(input("Digite a idade do funcionário: "))

        # Query corrigida seguindo o modelo do professor (sem repetições)
        str_insert = f"""INSERT INTO funcionarios (CPF, NOME, CARGO, SALARIO, IDADE) VALUES ({funcionario_cpf}, '{funcionario_nome}', '{funcionario_cargo}', {funcionario_salario}, {funcionario_idade})"""

        inst_SQL.execute(str_insert)
        conexao.commit()

    except ValueError:
        print("Erro: CPF, salário e idade devem ser númericos!")
    except Exception as erro:
        print(f"Erro: {erro}")
    else:
        print("Funcionário inserido com sucesso!")

def exibir_funcionarios(inst_SQL):
    lista_dados = []
    inst_SQL.execute("SELECT * FROM funcionarios")
    # capturar os registros do resultado da consulta
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    if len(lista_dados) == 0:
        print("Não há registros na tabela de funcionários.")
    else:
        df_dados = pd.DataFrame.from_records(
            lista_dados,
            columns=["Id", "CPF", "NOME", "CARGO", "SALARIO", "IDADE"],
            index="Id",
        )
        print("\n--- LISTA DE FUNCIONÁRIOS ---")
        print(df_dados)
        print("\n")

def alterar_funcionario(inst_SQL, conexao):
    exibir_funcionarios(inst_SQL)

    id_alterar = int(input("Digite o ID do funcionário que deseja alterar os dados: "))
    lista_dados = []

    str_consulta = f"""SELECT * FROM funcionarios WHERE ID = {id_alterar}"""
    inst_SQL.execute(str_consulta)
    # capturar os registros do resultado da consulta
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    # criar o dataframe a partir da lista
    df_dados = pd.DataFrame.from_records(lista_dados, columns=['Id', 'CPF','NOME', 'CARGO', 'SALARIO', 'IDADE'], index='Id')

    if (df_dados.empty):
        print("ID do funcionário não encontrado.")
    else:
        print(df_dados)
        try:
            funcionario_cpf = (int(input("Digite o novo CPF: ")))
            funcionario_nome = (input("Digite o novo nome: "))
            funcionario_cargo = (input("Digite o novo cargo: "))
            funcionario_salario = float(input("Digite o novo salário: "))
            funcionario_idade = (int(input("Digite a nova idade: ")))

            str_update = f"""UPDATE funcionarios
                             SET CPF={funcionario_cpf}, NOME='{funcionario_nome}',  CARGO='{funcionario_cargo}',
                                SALARIO={funcionario_salario}, IDADE={funcionario_idade}
                             WHERE ID = {id_alterar}"""

            inst_SQL.execute(str_update)
            conexao.commit()
        except ValueError:
            print("Erro: CPF, salário e idade devem ser numéricos!")
        except Exception as erro:
            print(f"Erro: {erro}")
        else:
            print("Dados alterados com sucesso!")

def excluir_funcionario(inst_SQL, conexao):
    exibir_funcionarios(inst_SQL)
    try:
        id_excluir = int(input("Digite o ID do funcionário que deseja excluir: "))

    except ValueError:
        print("O ID deve ser um número inteiro válido.")
        return
    
    lista_dados = []

    str_consulta = f"""SELECT * FROM funcionarios WHERE ID = {id_excluir}"""
    inst_SQL.execute(str_consulta)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if (len(lista_dados) == 0):
            print("ID do funcionário não encontrado.")
    else:
        try:
            str_delete = f"""DELETE FROM funcionarios WHERE ID = {id_excluir}"""
            inst_SQL.execute(str_delete)
            conexao.commit()
        except Exception as erro:
                print(f"Erro: {erro}")
        else:
            print("Funcionário excluído com sucesso!")

def relatorio_salario(inst_SQL):
    lista_dados = []
    str_consulta = "SELECT * FROM funcionarios WHERE SALARIO BETWEEN 8000 AND 12000"

    inst_SQL.execute(str_consulta)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if len(lista_dados) == 0:
        print("\nNão há funcionários com salário entre 8000 e 12000.\n")
    else:
        df_dados = pd.DataFrame.from_records(
            lista_dados,
            columns=["Id", "CPF", "NOME", "CARGO", "SALARIO", "IDADE"], 
            index="Id"
        )

        print(df_dados)
        df_dados.to_csv("relatorio_salarios.txt", sep="\t", encoding="utf-8")
        print("\nRelatório salvo com sucesso no arquivo 'relatorio_salarios.txt'!\n")

def relatorio_cargo_idade(inst_SQL):
    lista_dados = []
    str_consulta = "SELECT * FROM funcionarios WHERE LOWER(CARGO) = 'desenvolvedor front-end' AND IDADE > 26"

    inst_SQL.execute(str_consulta)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if len(lista_dados) == 0:
        print("\nNão há desenvolvedores front-end com mais de 26 anos.\n")
    else:
        lista_dados = sorted(lista_dados)
        df_dados = pd.DataFrame.from_records(
            lista_dados,
            columns=["Id", "CPF", "NOME", "CARGO", "SALARIO", "IDADE"],
            index="Id",
        )
        print(df_dados)
        df_dados.to_csv("relatorio_devs_idade.txt", sep="\t", encoding="utf-8")
        print("\nRelatório salvo com sucesso no arquivo 'relatorio_devs_idade.txt'!\n")

if __name__ == "__main__":
    main()