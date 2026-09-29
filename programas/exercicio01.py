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
            opcao = int(input("Digite a opção desejada (1 a 7): "))

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
        funcionario_nome = (input("Digite o CPF do funcionário: "))
        funcionario_salario = float(input("Digite o CPF do funcionário: "))
        funcionario_idade = int(input("Digite a idade do funcionário: "))
