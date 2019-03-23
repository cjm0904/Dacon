import pandas as pd
import matplotlib
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pandas import DataFrame
import json

# null값 0으로 채우기
df = DataFrame(pd.read_excel('Regular_Season_Batter.xlsx', sheet_name='Regular_Season_Batter'))
pre = DataFrame(pd.read_excel('Pre_Season_Batter.xlsx', sheet_name='Pre_Season_Batter'))

df['avg'] = df['avg'].fillna(0)
df['SLG'] = df['SLG'].fillna(0)
df['OBP'] = df['OBP'].fillna(0)
df['OPS'] = df['OPS'].fillna(0)
df = df.drop("team", 1)
df = df.drop("batter_name", 1)
df = df.drop("height/weight", 1)
df = df.drop("year_born", 1)
df = df.drop("position", 1)
df = df.drop("career", 1)
df = df.drop("starting_salary", 1)

pre['avg'] = pre['avg'].fillna(0)
pre['SLG'] = pre['SLG'].fillna(0)
pre['OBP'] = pre['OBP'].fillna(0)
pre['OPS'] = pre['OPS'].fillna(0)
pre = pre.drop("team", 1)
pre = pre.drop("batter_name", 1)
pre = pre.drop("height/weight", 1)
pre = pre.drop("year_born", 1)
pre = pre.drop("position", 1)
pre = pre.drop("career", 1)
pre = pre.drop("starting_salary", 1)

# 데이터 분류
testData = DataFrame(df).loc[df['year'] == 2018, :]
trnData = DataFrame(df).loc[df['year'] != 2018, :]


# corr = df.corr(method="pearson")
#
#
# print(corr['OPS']) # 타율(avg) : 0.92, 출루율(OBP) : 0.911, 장타율(SLG) : 0.97    기타 타격지표논 0.5 ~ 0.6


daybyday = pd.read_excel('Regular_Season_Batter_Day_by_Day.xlsx', sheet_name='Regular_Season_Batter_Day_by_Da')
daybyday['mydate'] = daybyday['year'].astype('str') + daybyday['date'].astype('str')

print(DataFrame(daybyday))


myData = daybyday[['batter_id', 'date', 'avg2']]
print(type(myData))
my = DataFrame(myData).loc[myData['batter_id'] == 0, :]
print(type(my))


#my.plot('date', 'avg2')



# print(daybyday[['batter_id', 'date', 'avg2']])
# print(daybyday['date'])



#print(corr.plot())

# P 196
# print(DataFrame(df['OPS']).corrwith(DataFrame(df['avg']), axis=1))

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


# print(crawling(2017, 3, 31))
# print(crawling(2017, 4, 1))


