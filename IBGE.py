import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def scrap_state_info(state:str) -> dict:
  """
  Retorna informações do estado brasileiro
  :param state: nome do estado
  :returns state_dict: dicionário com indicadores do estado
  """
  state_url = f'https://www.ibge.gov.br/cidades-e-estados/{state}.html'
  page = requests.get(state_url)

  soup = BeautifulSoup(page.content, 'html.parser')
  indicadors = soup.select('.indicador')

  state_dict = {
      ind.select('.ind-label')[0].text: ind.select('.ind-value')[0].text
      for ind in indicadors
  }

  state_dict['Estado'] = state
  return state_dict


scrap_state_info('sp')
states = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RO','RR','RS','SC','SP','SE','TO']

states_data = [scrap_state_info(state) for state in states]

df = pd.DataFrame(states_data)
states_df = df.copy()
states_df.columns = ['governor','capital','gentile','area','population','demographic_density','primary_school_enrollment','idh','revenues','expenditure','income_per_capita','vehicle_total','code']
states_df = states_df [['code','governor','population','area','idh','income_per_capita','vehicle_total','primary_school_enrollment','demographic_density','capital','gentile','revenues','expenditure']]
states_df = states_df.replace({
    '\.' : '',
    ',' : '.',
    '\[\d+\]' : '',
    'hab/km²': '',
    'km²': '',
    'pessoas': '',
    'matrículas': '',
    'R\$.*': '',
    'veículos' : ''
}, regex = True)

num_cols = ['population','area','idh','income_per_capita','vehicle_total','primary_school_enrollment','demographic_density','revenues','expenditure']
states_df[num_cols] = states_df[num_cols].apply(lambda x: x.str.strip())
states_df[num_cols] = states_df[num_cols].apply(pd.to_numeric)
states_df.head()
states_df.to_csv('IBGE.csv' , index = False)
