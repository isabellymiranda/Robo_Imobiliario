import requests
from bs4 import BeautifulSoup
from requests.api import head
from datetime import datetime
import csv



header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
}
csv_columns = ['nome','valor','categoria','tipo','quartos','banheiros','area','detalhes', 'logradouro']
csv_data = []
estados = ['ac','al','ap','am','ba','ce','df','es','go','ma','mt','ms','mg','pa','pb','pr','pe','pi','rj','rn','ro','rr','rs','sc','sp','se','to']


for estado in estados: 
    cont = 1
    
    while True:  
        url_estado = 'https://{}.olx.com.br/imoveis?o={}'.format(estado ,cont)
        requisicao = requests.get(url_estado , headers=header)
        soup = BeautifulSoup(requisicao.content, 'html.parser')
        

        if soup.select_one('div.sc-hmzhuo.kJjuHR.sc-jTzLTM.iwtnNi a') == None:
            break
        else:
            for imovel_url in soup.select('a.fnmrjs-0.fyjObc'): 
                imovel_url = imovel_url['href']

                dados = []
                
                
                requisicao_imovel = requests.get(imovel_url, headers=header)
                soup_imovel = BeautifulSoup(requisicao_imovel.content, 'html.parser')

                try:
                    nome_imovel = soup_imovel.select_one('h1.sc-45jt43-0.eCghYu.sc-ifAKCX.cmFKIN').text
                    nome_imovel = nome_imovel.replace('\n','').strip()
                    nome_imovel = nome_imovel.replace('.','').strip()
                    nome_imovel = nome_imovel.replace('//','').strip()
                    nome_imovel = nome_imovel.replace('¥¥','').strip()
                    nome_imovel = nome_imovel.replace('$$','').strip()
                    nome_imovel = nome_imovel.replace('/','').strip()
                    nome_imovel = nome_imovel.replace('+','').strip()
                    nome_imovel = nome_imovel.replace('-','').strip()
                    nome_imovel = nome_imovel.replace('!','').strip()
                    nome_imovel = nome_imovel.replace('?','').strip()
                    nome_imovel = nome_imovel.replace('#','').strip()
                    nome_imovel = nome_imovel.replace('*','').strip()
                    nome_imovel = nome_imovel.replace('´´','').strip()
                    nome_imovel = nome_imovel.replace('>','').strip()
                    nome_imovel = nome_imovel.replace('<','').strip()
                    nome_imovel = nome_imovel.replace('~','').strip()
                    nome_imovel = nome_imovel.replace(',','').strip()   
                   

                    
                    
                except:
                    nome_imovel = 'Não definido'
                    
                dados.append(nome_imovel)


                try:
                    valor = soup_imovel.select_one('div:nth-of-type(4) h2').string
                except:
                    valor = 'Não definido'
                dados.append(valor)
                

                categoria = 'Não definido'
                tipo = 'Não definido'
                quartos = 'Não definido'
                banheiros = 'Não definido'
                area = 'Não definido'
                detalhes = 'Não definido'
                logradouro = 'Não definido'

                for x in soup_imovel.select('div.duvuxf-0.h3us20-0.jyICCp'):    
                        
                    chave = x.select_one('dt').text

                    try:
                        valor = x.select_one('a').text
                    except:
                        valor = x.select_one('dd').text

                    if chave == "Categoria":
                        categoria = valor

                    elif chave == "Tipo":
                        tipo = valor

                    elif chave == "Quartos":
                        quartos = valor
                    
                    elif chave == "Banheiros":
                        banheiros = valor
                    
                    elif chave == "Área útil" or chave == "Área construída" or chave == "Tamanho" or chave == "Área total":
                        area = valor
                    
                    elif chave == "Detalhes do imóvel":
                        detalhes = valor
                    
                    elif chave == "Logradouro":
                        logradouro = valor

                dados.append(categoria)
                dados.append(tipo)
                dados.append(quartos)
                dados.append(banheiros)
                dados.append(area)
                dados.append(detalhes)
                dados.append(logradouro)

                csv_data.append(dados)

                print (dados)
                

            cont = cont +1

with open('Olx {}.csv'.format(datetime.now()) , 'a', encoding='utf-8') as f:

	writer = csv.writer(f, delimiter=';')

	writer.writerow(csv_columns ) 

	writer.writerows(csv_data)
