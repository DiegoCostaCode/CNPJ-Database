
# Desafio

Crie um sistema que persista informações sobre companhias abertas em um banco de dados e
permita consultar essas informações posteriormente. Note que esses dados podem mudar de
uma data para outra (DENOM_SOCIAL e SIT) e que o usuário gostaria de acessar informações
para uma determinada data.

## Requisitos

Por favor, rode o comando `pip install -r requirements.txt` para baixar as dependências do projeto. Você pode visualizar o arquivo requirements [aqui](https://github.com/DiegoCostaCode/SPART---CNPJ-CASE/blob/master/requirements.txt)


### Versão mínima do Python
PYTHON >= 3.12.4

### Bibliotecas e Instalação

As seguintes bibliotecas são necessárias:
* `oracledb` = Para conexão com banco de dados;
* `pandas` = Para melhor manipulação de código e arquivos;
* `tabulate` = Para uma melhor visualização do usuário;


## Configuração banco de dados

Para que o programa funcione corretamente, você precisa criar um arquivo chamado `database.properties` com as informações do seu banco de dados. O arquivo deve ter o seguinte formato:

* `user`: exemplo `teste123`
* `password`: exemplo `123teste`
* `host`: exemplo `oracle.teste`
* `port`: substitua pelo número de porta correto
* `service_name`: substitua pelo nome de serviço correto

Substitua as informações acima com as suas credenciais do banco de dados.

## Funções do projeto

- `conexaobd()`: Conexão com o banco de dados;
- `CreateTable()`: Cria a tabela COMPANHIAS no banco de dados;
- `LoadData()`: Carrega os dados do arquivo Excel no banco de dados;
- `Cnpjfilter()`: Faz um SELECT na tabela COMPANHIAS com base no CNPJ;
- `RazaoSocialfilter()`: Faz um SELECT na tabela COMPANHIAS com base na Razão Social;
- `Datefilter()`: Faz um SELECT na tabela COMPANHIAS com base na Data de Registro;
- `Read()`: Exibe todos os registros da tabela COMPANHIAS;
- `Menu()`: Exibe um menu para o usuário escolher uma opção de busca;
- `Main()`: Função principal do programa, inicializa a conexão com o banco de dados, cria a tabela se necessário, carrega os dados do arquivo Excel e exibe o menu para o usuário.

## Como usar

1. Assim que abrir o projeto em uma IDE de preferêncai, execute o comando `pip install -r requirements.txt` para baixar as dependências do projeto;
2. Crie o arquivo `database.properties` e insira suas credenciais de banco de dados;
3. Execute o arquivo `main.py` para iniciar o programa;
4. Siga as instruções do menu para consultar os dados;


**Autor Diego Costa Silva - diegocosta.contato2021@gmail.com**