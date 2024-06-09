#IMPORTS
import oracledb
import pandas as pd

#Carregando arquivos
df = pd.read_excel("cad_cia_aberta.xlsx")

#Importando tabelas importantes
df_columns = df[["CNPJ_CIA","DENOM_SOCIAL","SIT","DT_REG"]]

#Verificando dados faltantes:
print(df_columns.describe(include='all'))

def conexaobd():
    try:
        with open('database', 'r') as properties:
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

