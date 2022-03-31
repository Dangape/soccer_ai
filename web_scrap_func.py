import pandas as pd
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import os
import time


def scoresfixtures(link, ids):
    '''
    Description: This Class picks all the games that had in one season and combinate all links to one especific list
    Inputs:
        - link: The link of the main page that have all season games desired.
        - ids: The ID of the championship table
    Outputs:
        - especific list that has all the links of all matches of the season
    '''

    req = requests.get(link)
    if req.status_code == 200:
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    tb = soup.find(id=ids)

    s1 = []
    s2 = []
    for i in tb.find_all("a"):
        s1.append(str(i))
        s2.append(str(i.get_text('href')))

    # Calling DataFrame constructor after zipping
    # both lists, with columns specified
    di = pd.DataFrame(list(zip(s1, s2)),
                      columns=['Codes', 'ID'])

    s4 = []
    for i in di["Codes"]:
        i = i.replace('<a href="', '')
        i = i.replace('</a>', '')
        s4.append(str(i))

    s5 = []

    for i in di['Codes']:
        if "matches" in i:
            s5.append(str(i))
        else:
            s5.append(0)

    s6 = []
    for i in di["Codes"]:
        if '<a href="/en/squads/' in i:
            i = i.replace('<a href="/en/squads/', '')
            i = i[0:8]
            s6.append(str(i))
        else:
            s6.append(0)

            # Calling DataFrame constructor after zipping
    # both lists, with columns specified
    da = pd.DataFrame(list(zip(s1, s2, s4, s5, s6)),
                      columns=['CODES', 'ID', 'URL_FINAL', 'PARTIDAS_2019', "TEAM_CODE"])

    s9 = []
    for i in da["URL_FINAL"]:
        if 'Match Report' in i:
            s9.append(str(i))
        else:
            pass
    return s9


def planilhas(url):
    '''
    Description: This function goes to de URL of the match and treat all data in order to append it in one single Dataframe.
    Input:
        - url: Url of the html page
    Output:
        - Dataframe treated from the match saved on my machine excel file
    '''

    # make the request
    pg = 'https://fbref.com'
    url_pg = pg + url
    req = requests.get(url_pg)
    if req.status_code == 200:
        content = req.content
    # accessing data from site
    soup = BeautifulSoup(content, 'html.parser')

    table_geral = soup.find_all(class_="table_container")
    table_time_1 = table_geral[0]
    table_time_2 = table_geral[2]
    table_time_3 = soup.find(class_='venuetime')

    # collecting data

    table_torcida = soup.find_all('div', class_="scorebox_meta")
    oi_torcida = str(table_torcida)

    # treating data
    toby = oi_torcida.split('<small>')
    torcida = str(toby[2])
    torcida = torcida.split('</small>')
    torcida = str(torcida[0])
    estadio = toby[4]
    estadio = estadio.split('</small>')
    estadio = str(estadio[0])

    # collecting data
    data = table_time_3.get('data-venue-date')

    # treating data
    nome = str(soup.title)
    nome = nome.replace(" ", "_")
    nome = nome.replace("<title>", "")
    nome = nome.replace(".", "")
    nome_final = nome.split("Report")[0]

    # treating data

    nome_final = nome_final.split("_Match")
    nome_final = nome_final[0]

    # STR transform and reading tables
    table_str_1 = str(table_time_1)
    table_str_2 = str(table_time_2)
    df_1 = pd.read_html(table_str_1)[0]
    df_2 = pd.read_html(table_str_2)[0]

    # treating data

    time = str(nome_final)
    time = time.replace("_", " ")
    time = time.split(" vs ")
    time_1 = str(time[0])
    time_2 = str(time[1])

    # Dtframe transforming
    df_1 = pd.DataFrame(df_1)
    df_1.columns = df_1.columns.droplevel()
    df_1['Time'] = str(time_1)
    df_1['Time_Adversario'] = str(time_2)
    df_1['Confronto'] = str(nome_final)
    df_1['Data'] = str(data)
    df_1['Estadio'] = str(estadio)
    df_1['Torcida'] = torcida

    df_2 = pd.DataFrame(df_2)
    df_2.columns = df_2.columns.droplevel()
    df_2['Time'] = str(time_2)
    df_2['Time_Adversario'] = str(time_1)
    df_2['Confronto'] = str(nome_final)
    df_2['Data'] = str(data)
    df_2['Estadio'] = str(estadio)
    df_2['Torcida'] = torcida

    # APPENDING Dataframes
    df_3 = df_1.append(df_2)

    # save excel
    writer = pd.ExcelWriter("C:/Users/DANIEL BEMERGUY/OneDrive/soccer_ai/Data/2017_A/"+nome_final + '.xlsx')
    df_3.to_excel(writer, "Estatisticas")
    writer.save()


def tratamento(nome):
    '''
    Description: This function goes through all files of the directiory and joins all them in one single dataframe saving in
    excel sheet.
    Input:
        - Nome: Name that you want for your excel sheet
    Output:
        - Dataframe of all games save as excel sheet
    '''
    path = "C:/Users/DANIEL BEMERGUY/OneDrive/soccer_ai/Data/2017_A/"
    entries = os.listdir(path)
    base = {}
    base = pd.DataFrame(base)

    for i in entries:
        if "xlsx" in i:
            base = base.append(pd.read_excel(path + i))
            base = base.drop_duplicates()
        # escrevendo em excelfile
        else:
            pass

    writer = pd.ExcelWriter("C:/Users/DANIEL BEMERGUY/OneDrive/soccer_ai/Data/Treated/" + nome + ".xlsx")
    base.to_excel(writer, nome)
    writer.save()


