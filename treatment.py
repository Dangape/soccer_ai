import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from web_scrap_func import *

years = ['2016', '2017', '2018','2019', '2020', '2021']
division = '1'
df = get_mkt_infos(years,division)
df = df.apply(lambda x: x.str.replace(',', '.'))
df.value = df.value.astype(float)
df.player_amt = df.player_amt.astype(float)

df['value_per_player'] = df.value / df.player_amt

# save excel
nome_final = 'mkt_infos_' + division
writer = pd.ExcelWriter("C:/Users/DANIEL BEMERGUY/OneDrive/soccer_ai/Data/Treated/" + nome_final + '.xlsx')
df.to_excel(writer, "Estatisticas")
writer.save()
