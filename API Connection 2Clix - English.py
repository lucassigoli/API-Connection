#SUMMARY:
#The program will connect with the 2Clix API to collect Monitoring and Quality data
#He logs in and captures the token. The token I will use in the headers of my request. Whenever I make a request I need this token.
#It checks if the file we want to download exists in the Monitoring and Quality folder. 
#If it doesn't exist I'll go down, if it exists I won't go down


#IMPORTING THE NECESSARY LIBRARIES
import requests
import json
import os
import pandas as pd
from datetime import date, datetime, timedelta
import csv

#ACCESS DATA
login = "XXXXX" #I changed the login and the password for data safety
senha = "XXXXX"
url_login = "https://api.2clix.com.br/v3/Usuario/login"
url_tabela = "https://api.2clix.com.br/v3/Reports/AnaliticoAvaliacoes?Dtinicio=2024-07-01&DtFim="

#ENTRY PARAMETERS
data_inicio = date(2024, 7, 1) # 01-01-2024, here you write the first extracting day
data_fim = date.today() - timedelta(days=1) #last extracting day (yesterday)
horario_inicio = "T00:00:00" #start time
horario_fim = "T23:59:59" #end time
usuario_logado = os.getlogin() #takes the computer user name to always make the folder path work 

#SUPPORT FUNCTIONS

#TOKEN FUNCTION
def generate_access_token (url_login):
    
    #Defining the dictionary to make the payload to the server 
    payload = {
        "login": login,
        "senha": senha
    }

    #Defining the headers dictionary to inform the server that we sending the data in JSON format. Otherwise the API can understand it wrongly.
    headers = {
        "Content-Type": "application/json" #Avoids errors
    }

    response = requests.post(url_login, headers=headers, data=json.dumps(payload), verify = False)

    if response.status_code == 200:
        print("Login bem sucedido!")
        token = response.json().get("token")
    else:
        print(f"Login falhou! O erro gerado foi: {response.status_code}")
    return token

#Getting the token
token = generate_access_token(url_login)

#Defining my new headers, it will be my token
headers = {
    "Authorization": f"Bearer {token}",
}

while data_inicio <= data_fim:
    
    data_inicio_str = str(data_inicio) #Transforming it in string to concatenate the url 
    urlfinal = "https://api.2clix.com.br/v3/Reports/AnaliticoAvaliacoes?DtinicioAtualizacao=" + data_inicio_str + horario_inicio + "&DtFimAtualizacao=" + data_inicio_str + horario_fim + "&codTipoFicha=1&ExibeSituacaoMonitoria=0"
    folder_path = fr"C:\Users\{usuario_logado}\SASCAR\Suporte as Operações - Dados\Bases\Extração API Python\MonitoriaQualidade"
    
    file_path = os.path.join(folder_path, f"Qualidade_{data_inicio}.json") #Attaching the archive name to my folder path. 
    
    if not os.path.exists(file_path):
        response = requests.get(urlfinal, headers = headers, verify = False)
        dados_tabela = response.json() #Getting the JSON archive trough the JSON variable. 

        if dados_tabela is not None:
            json_str = json.dumps(dados_tabela) #Transforming in string the "dados tabela" archive (it's as any) .
            dados_tabela = json.loads(json_str) #Transform the json_str(a string) in a JSON archive.
            print(json_str)
            
            #We save the JSON archive and we save it in the destination folder. 
            with open (file_path, mode = "w", encoding="utf-8") as f:
                json.dump(dados_tabela, f, ensure_ascii = False, indent = 4)
            print("Arquivo Salvo")
    else:
        print(f"O arquivo Monitoria_{data_inicio_str}ja existe")

    data_inicio += timedelta(days=1)
    print(data_inicio)