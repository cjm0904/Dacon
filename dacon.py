import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pandas import DataFrame
import json

# null값 0으로 채우기
df = DataFrame(pd.read_excel('Regular_Season_Batter.xlsx', sheet_name='Regular_Season_Batter'))
df['avg'] = df['avg'].fillna(0)
df['SLG'] = df['SLG'].fillna(0)
df['OBP'] = df['OBP'].fillna(0)


# 웹크롤링 시작
# 출처 : http://www.statiz.co.kr

def crawling(year, month, date):
    result = []
    if month < 10:
        month = '0'+ str(month)
    if date < 10:
        date = '0' + str(date)

    url = "http://www.statiz.co.kr/boxscore.php?date="
    url = url + str(year) + '-'+ str(month) + '-' + str(date)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all("table", {"class":"table table-striped no-space table-bordered"})
    if data is None:
        return None
    for i in data:
        team = i.find_all("td",{"style":"text-align:center;padding-top:3px;padding-bottom:3px;"})
        awayTeam = team[0].get_text()
        homeTeam = team[1].get_text()

        score = i.find_all("td", {"style": "padding-top:3px;padding-bottom:3px;text-align:center;"})
        awayScore = score[0].get_text()
        homeScore = score[score.__len__()-1].get_text()

        result.append(json.dumps({"awayTeam": awayTeam, "homeTeam": homeTeam, "awayScore": awayScore, "homeScore": homeScore}, ensure_ascii=False))
    return result


print(crawling(2017, 3, 31))
print(crawling(2017, 4, 1))