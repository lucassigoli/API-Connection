#RESUMO:
#O programa ira se conectar com a API da 2Clix para coletar os dados de Monitoria e Qualidade
#Ele faz o login e captura o token. O token eu vou utilizar no headers do meu request. Sempre que
#eu fizer um request eu preciso desse token.
#Ele verifica se na pasta Monitoria e Qualidade existe o arquivo que queremos baixar. Se nao exister eu baixo, se existir eu nao baixo
#A documentacao da API esta com o Lucas Santos de dados

#IMPORTANDO AS BIBLIOTECAS NECESSARIAS
import requests
import json
import os
import pandas as pd
from datetime import date, datetime, timedelta
import csv

#DADOS DE ACESSO
login = "22975"
senha = "Lu17021988**"
url_login = "https://api.2clix.com.br/v3/Usuario/login"
url_tabela = "https://api.2clix.com.br/v3/Reports/AnaliticoAvaliacoes?Dtinicio=2024-07-01&DtFim="

#PARAMETROS DE ENTRADA
data_inicio = date(2024, 7, 1) # 01-01-2024, aqui voce pode alterar o dia de inicio da coleta dos dados
data_fim = date.today() - timedelta(days=1) #data de fim da extracao (ontem)
horario_inicio = "T00:00:00"
horario_fim = "T23:59:59"
usuario_logado = os.getlogin() #pega o nome do usuario logado para ele sempre achar o caminho do arquivo

#FUNCOES PARA DAR SUPORTE AO PROGRAMA

#FUNCAO TOKEN
def generate_access_token (url_login):
    
    #Definindo o dicionario para fazer o payload para o servidor
    payload = {
        "login": login,
        "senha": senha
    }

    #Definindo o dicionario headers (cabecalho) para informar ao servidor que estamos enviando os dados no tipo JSON. Caso contario o serviodr pode interpretar de forma errada.
    headers = {
        "Content-Type": "application/json" #Isso serve para evitar erros
    }

    response = requests.post(url_login, headers=headers, data=json.dumps(payload), verify = False)

    if response.status_code == 200:
        print("Login bem sucedido!")
        token = response.json().get("token")
    else:
        print(f"Login falhou! O erro gerado foi: {response.status_code}")
    return token

#Invocando a funcao generate_access_token para pegarmos o nosso token
token = generate_access_token(url_login)

#Definindo o meu novo headers, ele vai ser o meu token
headers = {
    "Authorization": f"Bearer {token}",
}

while data_inicio <= data_fim:
    
    data_inicio_str = str(data_inicio) #transformando em string para poder concatenar a url
    urlfinal = "https://api.2clix.com.br/v3/Reports/AnaliticoAvaliacoes?DtinicioAtualizacao=" + data_inicio_str + horario_inicio + "&DtFimAtualizacao=" + data_inicio_str + horario_fim + "&codTipoFicha=1&ExibeSituacaoMonitoria=0"
    folder_path = fr"C:\Users\{usuario_logado}\SASCAR\Suporte as Operações - Dados\Bases\Extração API Python\MonitoriaQualidade"
    
    file_path = os.path.join(folder_path, f"Qualidade_{data_inicio}.json") #Anexando o meu nome do arquivo ao caminho da pasta
    
    if not os.path.exists(file_path):
        response = requests.get(urlfinal, headers = headers, verify = False)
        dados_tabela = response.json() #Captura o arquivo json da variavel json

        if dados_tabela is not None:
            json_str = json.dumps(dados_tabela) #Transforma em string o arquivo dados tabela (ele esta como any)
            dados_tabela = json.loads(json_str) #Transforma o json_str(uma string) em arquivo json
            print(json_str)
            
            #Salvamos o arquivo em JSON e salvamos na pasta de destino
            with open (file_path, mode = "w", encoding="utf-8") as f:
                json.dump(dados_tabela, f, ensure_ascii = False, indent = 4)
            print("Arquivo Salvo")
    else:
        print(f"O arquivo Monitoria_{data_inicio_str}ja existe")

    data_inicio += timedelta(days=1)
    print(data_inicio)