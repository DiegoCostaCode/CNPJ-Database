"""
    Diego Costa Silva - diegocosta.contato2021@gmail.com

    Detalhe:

    Por favor, execute em seu console: 
    >>> pip install -r requirements.txt
"""

#Imports
import oracledb
import pandas as pd
import datetime
from tabulate import tabulate 

#Carregando arquivos
df = pd.read_excel("cad_cia_aberta.xlsx")

#Importando tabelas importantes
df_columns = df[["CNPJ_CIA","DENOM_SOCIAL","SIT","DT_REG"]]

def conexaobd():

    """
    Esta função faz conexão com o banco de dados, puxando os 
    parâmetros colocados no arquivo database.properties.

    Retorna uma conexão com o banco de dados se a conexão for bem-sucedida, 
    ou None caso contrário.
    """

    try:
        with open('database.properties', 'r') as properties:
            credentials = {}
            for line in properties:
                key, value = line.strip().split('=')
                credentials[key] = value
        conn = oracledb.connect(
            user=credentials['user'],
            password=credentials['password'],
            host=credentials['host'],
            port=int(credentials['port']),
            service_name=credentials['service_name'],
        )
        return conn
    
    except oracledb.DatabaseError as error:
        print(f"Erro ao conectar ao Banco de Dados: {error}")
        return None
    
def CreateTable(conn):

    """
    Verifica se a tabela COMPANHIAS existe no banco de dados e, 
    se não existir, cria uma.

    Args:
        conn: conexão com o banco de dados
    """

    print("Criando a tabela em seu banco de dados...")
    try:
        
        cursor = conn.cursor()

        table_verify = str("SELECT * FROM COMPANHIAS")

        script = str("""
                CREATE TABLE COMPANHIAS (
                ID NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
                CNPJ VARCHAR2(20),
                RAZAO_SOCIAL VARCHAR2(100),
                STATUS VARCHAR2(26),
                DATA_REGISTRO DATE)
                """)
       
        if not table_verify:
            cursor.execute(script)
            conn.commit() 
            print("Tabela criada com sucesso!") 
                
    except Exception as error:
        print(f"Erro: {error}")

def LoadData(conn, df_columns):

    """
        Carrega os dados do arquivo Excel no banco de dados.

        Verifica se os dados do arquivo Excel já existem no banco de dados,
        e se não existirem, os insere.

        Args:
            conn: conexão com o banco de dados
            df_columns: dados do arquivo Excel
    """

    try:
        cursor = conn.cursor()
        script_insert = str("""
            INSERT INTO COMPANHIAS (CNPJ, RAZAO_SOCIAL, STATUS, DATA_REGISTRO)
            VALUES (:CNPJ, :RAZAO_SOCIAL, :STATUS, :DATA_REGISTRO)
        """)
        script_check = str("""
            SELECT CNPJ, RAZAO_SOCIAL, STATUS, DATA_REGISTRO 
            FROM COMPANHIAS
        """)

        cursor.execute(script_check)
        existing_data = cursor.fetchall()
        existing_data_set = set((row[0], row[1], row[2], row[3]) for row in existing_data)
        
        data_to_insert = [row for row in df_columns.values.tolist() if (row[0], row[1], row[2], row[3]) not in existing_data_set]
        
        if data_to_insert:
            cursor.executemany(script_insert, data_to_insert)
            conn.commit()
            print("Dados carregados com sucesso!")
        else:
            print("Tudo pronto!!!")

    except Exception as error:
        print(f"Erro: {error}")

def Cnpjfilter(conn, column, value):

    """
    Faz um SELECT na tabela COMPANHIAS com base no CNPJ.

    Args:
        conn: conexão com o banco de dados
        column: coluna a ser filtrada (CNPJ)
        value: valor a ser buscado

    Retorna os resultados da consulta.
    """
     
    try:
        cursor = conn.cursor()

        script = str(f"SELECT * FROM COMPANHIAS WHERE {column} = :value")

        cursor.execute(script, {"value": value})

        rows = cursor.fetchall()

        if rows:
            print("\nResultados:")
            headers = ["ID", "CNPJ", "Razão Social", "Status", "Data de Registro"]
            print(tabulate(rows, headers, tablefmt="grid"))
            print("\n")
        else:
            print(f"\nNenhum registro encontrado para {value}.\n Verifique novamente o valor inserido.\n")

    except Exception as error:
        print(f"Erro ao ler dados: {error}")

def RazaoSocialfilter(conn, column, value):

    """
    Faz um SELECT na tabela COMPANHIAS com base na Razão Social.

    Args:
        conn: conexão com o banco de dados;
        column: coluna a ser filtrada (Razão Social);
        value: valor a ser buscado.

    Retorna os resultados da consulta.
    """

    try:
        cursor = conn.cursor()

        script = str(f"SELECT * FROM COMPANHIAS WHERE {column} = :value")

        cursor.execute(script, {"value": value})

        rows = cursor.fetchall()

        if rows:
            print("\nResultados:")
            headers = ["ID", "CNPJ", "Razão Social", "Status", "Data de Registro"]
            print(tabulate(rows, headers, tablefmt="grid"))
            print("\n")
        else:
            print(f"\nNenhum registro encontrado para {value}.\n Verifique novamente o valor inserido.\n")

    except Exception as error:
        print(f"Erro ao ler dados: {error}")

def Datefilter(conn, column, initialDate, finalDate):

    """
    Faz um SELECT na tabela COMPANHIAS com base na Data de Registro inserida pelo usuario.

    Args:
        conn: conexão com o banco de dados;
        column: coluna a ser filtrada (Data de Registro);
        initialDate: data inicial inserida pelo usuário;
        finalDate: data final do período inserida pelo usuário.

    Retorna os resultados da consulta.
    """

    try:
        cursor = conn.cursor()

        script = str(f"SELECT * FROM COMPANHIAS WHERE {column} BETWEEN :initialDate AND :finalDate")

        cursor.execute(script, {"initialDate":  initialDate, "finalDate": finalDate})

        rows = cursor.fetchall()

        if rows:
            print("\nResultados:")
            headers = ["ID", "CNPJ", "Razão Social", "Status", "Data de Registro"]
            print(tabulate(rows, headers, tablefmt="grid"))
            print("\n")
        else:
            print(f"\nNenhum registro encontrado para o periodo de {initialDate} a {finalDate}.\n")

    except Exception as error:
        print(f"Erro ao ler dados: {error}")

def Read(conn):


    """
    Exibe todos os registros da tabela COMPANHIAS.

    Args:
        conn: conexão com o banco de dados
    """


    try:
        cursor = conn.cursor()

        script = str(f"SELECT * FROM COMPANHIAS ORDER BY ID ASC")

        cursor.execute(script)

        page_size = 20
        rows = cursor.fetchmany(page_size)
        print("\nBanco de dados:")
        headers = ["ID", "CNPJ", "Razão Social", "Status", "Data de Registro"]
        print(tabulate(rows, headers, tablefmt="grid"))

        while True:
            resposta = str(input("Deseja ver mais linhas? (s/n): "))
            if resposta.lower() == 's':
                rows = cursor.fetchmany(page_size)
                if rows:
                    print(tabulate(rows, headers, tablefmt="grid"))
                else:
                    print("Não há mais linhas para mostrar.")
                    break
            elif resposta.lower() == 'n':
                print("Okay, estes são os resultados.\n")
                break
            else:
                print("Resposta inválida. Tente novamente :D.")

    except Exception as error:
        print(f"Erro ao ler dados: {error}")

def Menu(conn):

    """
    Exibe um menu para o usuário escolher uma opção de busca.

    Args:
        conn: conexão com o banco de dados
    """

    print("\n")
    while True:
        try:
            print(">>>\n Por favor, escolha uma opção de 1 a 4 ou 0 para voltar: \n")
            column = int(input(" 1-Visualizar banco de dados; \n 2- Buscar por CNPJ; \n 3- Buscar por Razão Social \n 4- Buscar por Data de Registro\n 0- Sair\n"))
            match column:
                
                case 1:
                    Read(conn)
                case 2:
                    value = str(input("\nDigite o CNPJ, Exemplo: 01.234.567/8910-11\n<Digite 0 para voltar\n"))
                    Cnpjfilter(conn, "CNPJ", value)   

                case 3:
                    value = str(input("Digite a Razão Social: \n <Digite 0 para voltar\n"))
            
                    if value == 0:
                        break

                    RazaoSocialfilter(conn, "RAZAO_SOCIAL", value)

                case 4:
                            print("Digite o periodo de tempo que deseja buscar: \n<Digite 0 para voltar \n")
                            initialDate = str(input("Data inicío: \n"))
                            finalDate = str(input("Data final: \n"))

                            try:
                                initialDate = datetime.datetime.strptime(initialDate, "%d/%m/%Y")
                                finalDate = datetime.datetime.strptime(finalDate, "%d/%m/%Y")

                                if initialDate > datetime.datetime.now() or finalDate > datetime.datetime.now():
                                    print("\nErro: Data não pode estar no futuro! Data atual: " + datetime.datetime.now().strftime("%d-%m-%Y") + "\n")
                                elif initialDate > finalDate:
                                    print("\nErro: Data início não pode ser maior que a data final! \n")
                                else:
                                    Datefilter(conn, "DATA_REGISTRO", initialDate, finalDate)
                                    
                            except ValueError:
                                print("Erro: Data inválida! Use o formato dd/mm/yyyy")
    
                case _:
                    print("<<< Tchau... :(")
                    break

        except Exception as error:
            print(f"Erro:{error}")

def Main():

    """
    Função principal do programa.

    Inicializa a conexão com o banco de dados, cria a tabela se necessário,
    carrega os dados do arquivo Excel e exibe o menu para o usuário.
    """

    try:
      conn = conexaobd()

      print("=====Bem-vindo(a)=====\n")
      
      CreateTable(conn)

      LoadData(conn,df_columns)

      Menu(conn)

    except Exception as error:
        print(f"Erro: {error}")

if __name__ == "__main__":
    Main()
