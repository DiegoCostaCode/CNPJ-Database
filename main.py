#IMPORTS
import oracledb
import pandas as pd

#Carregando arquivos
df = pd.read_excel("cad_cia_aberta.xlsx")

#Importando tabelas importantes
df_columns = df[["CNPJ_CIA","DENOM_SOCIAL","SIT","DT_REG"]]

def conexaobd():
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
            service_name=credentials['service_name']
        )
        return conn
    
    except oracledb.DatabaseError as error:
        print(f"Erro ao conectar ao Banco de Dados: {error}")
        return None
    
def CreateTable(conn):
    print("Criando a tabela em seu banco de dados...")
    try:
        
        cursor = conn.cursor()

        table_verify = "SELECT * FROM COMPANHIAS"

        script = """
                CREATE TABLE COMPANHIAS (
                ID NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
                CNPJ VARCHAR2(20),
                RAZAO_SOCIAL VARCHAR2(100),
                STATUS VARCHAR2(26),
                DATA_REGISTRO DATE)
                """
       
        if not table_verify:
            cursor.execute(script)
            conn.commit() 
            print("Tabela criada com sucesso!") 
                
    except Exception as error:
        print(f"Erro: {error}")


def LoadData(conn, df_columns):
    try:
        cursor = conn.cursor()
        script_insert = """
            INSERT INTO COMPANHIAS (CNPJ, RAZAO_SOCIAL, STATUS, DATA_REGISTRO)
            VALUES (:CNPJ, :RAZAO_SOCIAL, :STATUS, :DATA_REGISTRO)
        """
        script_check = """
            SELECT CNPJ, RAZAO_SOCIAL, STATUS, DATA_REGISTRO 
            FROM COMPANHIAS
        """
        cursor.execute(script_check)
        existing_data = cursor.fetchall()
        existing_data_set = set((row[0], row[1], row[2], row[3]) for row in existing_data)
        
        data_to_insert = [row for row in df_columns.values.tolist() if (row[0], row[1], row[2], row[3]) not in existing_data_set]
        
        if data_to_insert:
            cursor.executemany(script_insert, data_to_insert)
            conn.commit()
            print("Dados carregados com sucesso!")
        else:
            print("Não há dados novos para serem carregados.")
    except Exception as error:
        print(f"Erro: {error}")

def Menu():
    while True:
        try:
            option = int(input("Por favor, escolhe uma opção de 1 a 5:"))
            match option:
                case 1:
                    print("Okay")
                    
                case 2:
                    print("Okay")

                case 3:
                    print("Okay")

                case 4:
                    print("Okay")
                case 5:
                    print("Okay")
                case _:
                    print("Okay")

        except Exception as error:
            print(f"Erro:{error}")

def Main():
    try:
      conn = conexaobd()

      print("=====Bem-vindo(a)=====")
      
      CreateTable(conn)

      LoadData(conn,df_columns)

      Menu()

    except Exception as error:
        print(f"Erro: {error}")

if __name__ == "__main__":
    Main()

