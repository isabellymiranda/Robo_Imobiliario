from datetime import datetime
import csv
import requests
from bs4 import BeautifulSoup
from lxml import html

def filtrar_text(obj_select, string):
	if type(obj_select) != list:
		array_find = [text for text in obj_select.find_all(text=True) if string in text]
	else:
		array_find = [text for text in obj_select if string in text]

	if array_find != []:
		return str(array_find[0]).replace(string, '').strip()
	else:
		return ''

csv_columns = ['name','appraised value','minimum sale value','real estate type','real estate situation','total area','private area','land area','address','description','payments']
csv_data = []
states = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RO','RR','RS','SC','SP','SE','TO']
cont = 0
for state in states:
	url_state = 'https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_{}.htm'.format(state)
	requisition = requests.get(url_state)
	soup = BeautifulSoup(requisition.content, 'html.parser')
	for property in soup.select('p.MsoNormal u span a'):
			property_url = property['href']
			if property_url != '#':
				if cont%2==0:
					
					property = []

					requisition_property = requests.get(property_url)
					soup_property = BeautifulSoup(requisition_property.content, 'html.parser')
					name = soup_property.select_one('div.control-item.control-span-12_12 h5')
					if name!= None:
						name_text = name.text.replace('\n','').strip()
						name_text = name.text.replace('O imóvel que você procura não está mais disponível para venda.','').strip()
						name_text = name_text.replace('Imóvel em disputa','').strip()

						print(name_text)
					else:
						name_text = ''

					property.append(
						name_text
					)

					valuation_value = soup_property.select_one('div.content-wrapper.clearfix div.content p')
					if valuation_value!= None:
						valuation_value = filtrar_text(valuation_value, 'Valor de avaliação: R$')
						
					else:
						valuation_value = ''

					property.append(
						valuation_value
					)
					
					minimum_value = soup_property.select_one('div.content-wrapper.clearfix div.content p')
					if minimum_value!= None:
						minimum_value = filtrar_text(minimum_value, 'Valor mínimo de venda: R$')
	
						print(minimum_value)
						
					else:
						minimum_value = ''

					property.append(
						minimum_value
					)
						
						

					type_property = soup_property.select_one('div.control-item.control-span-6_12 p')
					if type_property!= None:
						type_property = type_property.text.split('\n')
						type_of_property = filtrar_text(type_property, 'Tipo de imóvel:')
						
						
						print(type_of_property)
						
						
					else:
						type_of_property = ''
						
				
					property.append(
						type_of_property
				
					)
					situation_property = soup_property.select_one('div.control-item.control-span-6_12 p')
					if situation_property!= None:
						situation_property = situation_property.text.split('\n')
						situation_property = filtrar_text(situation_property, 'Situação:')
						
					
						print(situation_property)
						
					else:
						
						situation_property = ''
					
					
					property.append(
						situation_property
					)
					

					area_find = soup_property.select('div.control-item.control-span-6_12:nth-of-type(2) p span')
					if area_find!= None:
						area_find = [span.text for span in area_find]

						area_total = filtrar_text(area_find, 'Área total = ')
						area_private = filtrar_text(area_find, 'Área privativa =')
						area_land = filtrar_text(area_find, 'Área do terreno =')

						print (area_total)
						print (area_private)
						print (area_land)
					else:
						area_total = ''
						area_private = ''
						area_land = ''

					property.append(
						area_total
					)
					
					property.append(
						area_private
					)
					
					property.append(
						area_land
					)

					address = soup_property.select_one('div.related-box p:nth-of-type(1)')
					if address!= None:
						address_text = address.text.replace('\n','').strip()
						address_text = address.text.replace('Endereço:','').strip()

						print(address_text)
					else:
						address_text = ''

					property.append(
						address_text
					)

					description = soup_property.select_one('div.related-box p:nth-of-type(2)')
					if description!= None:
						description = description.text.split('\n')
						description = filtrar_text(description, 'Descrição:')
						description = description.replace('.','').strip()

						print(description)
					else:
						description = ''

					property.append(
						description
					)

					payment = soup_property.select_one('div.related-box p:nth-of-type(3)')
					if payment!= None:
						payment_text = payment.text.replace('\n','').strip()
						payment_text = payment.text.replace('Imóvel','').strip()

						print(payment_text)
					else:
						payment_text = ''

					property.append(
						payment_text
					)

					csv_data.append(
						property 
					)

					print ()	
					
				cont=cont+1

with open('casas-em-leilão-caixa {}.csv'.format(datetime.now()) , 'a', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter=';')

	writer.writerow(csv_columns ) 

	writer.writerows(csv_data)