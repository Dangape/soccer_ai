from web_scrap_func import *
import time

'''
Codes:
2017 - div_sched_1559_1
2018 - div_sched_1760_1
2019 - div_sched_3320_1
2020 - div_sched_10072_1
2021 - div_sched_10986_1
'''
start = time.time()

for url in scoresfixtures("https://fbref.com/en/comps/24/1760/schedule/2018-Serie-A-Scores-and-Fixtures","div_sched_1760_1"):
    print(url)
    planilhas(url)


tratamento("Brasileirao-2018")

print('Duration: {} seconds'.format(time.time() - start))

