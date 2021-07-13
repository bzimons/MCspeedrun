from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
from time import sleep
from datetime import datetime
from os import walk
# driver = webdriver.Chrome(ChromeDriverManager().install())


_,_,files = next(walk('D:\\foque\\unb\\proj\\MCspeedrun\\board')) #
arq = sorted(files,reverse=True)[0]

base= pd.read_csv('D:\\foque\\unb\\proj\\MCspeedrun\\board\\'+arq,sep=",")

userlink = (base['userlink'])[0:450] 

print(userlink)
datas=[]
game =[]
times =[]
playername=[]

for i in userlink:
    playerlink = i
    browser = webdriver.Chrome(executable_path="C:/Users/bolin/.wdm/drivers/chromedriver/win32/91.0.4472.101/chromedriver.exe")
    sleep(1.5)
    browser.get(playerlink)
    sleep(10)

    print(i)
    try:
        browser.find_element_by_xpath('''/html/body/main/div/div[2]/div[2]/div/div[2]/span/span[1]''').click()
        sleep(5)
        browser.find_element_by_xpath('''/html/body/main/div/div[2]/div[2]/div/div[2]/span/span[2]/label[2]/span''').click()
        sleep(8)
    except:
        pass

    respData = browser.page_source
    browser.close()
    sleep(5)
    soup = BeautifulSoup(respData, 'html.parser')
    table = soup.find( "table")

    player = re.sub('https://www.speedrun.com/user/','',playerlink)

    all_date=[]
    for i in table.findAll('time',class_="short circa"):
        if i.has_attr('datetime'):
            date = i['datetime']
            all_date.append(date)

    datas.extend(all_date)

    game_type=[]
    player_name_unique=[]
    for i in table.findAll('td',class_="center-sm-up top"):
        game_type.append(i.text)
        player_name_unique.append(player)

    playername.extend(player_name_unique)
    game.extend(game_type)


    in_game_time=[]
    for i in table.findAll('td',class_="nobr hidden-xs center")[1::4]:
        in_game_time.append(i.text)

    times.extend(in_game_time)
    try:
        df_player=pd.DataFrame({'Username':player_name_unique,'Game':game_type,'In-game-time':in_game_time,'Date':all_date})
        RSG16=df_player['Game'].str.contains(r'Any% Glitchless - Random Seed, 1.16+',na=False)
        df_player = df_player[RSG16]
        df_player['Date'] = df_player['Date'].str.replace(r'T12:00:00Z', '')
        df_player['In-game-time'] = df_player['In-game-time'].str.replace(r'(in-game time)', '')
        df_player['Game'] = df_player['Game'].str.replace(r'\n', '')
        path = r'''D:\Foque\unb\proj\MCspeedrun\players\\''' + player + '.csv'
        df_player.to_csv(path,sep=";")
    except:
        pass
     


df = pd.DataFrame({'Username':playername,'Game':game,'In-game-time':times,'Date':datas})
RSG16=df['Game'].str.contains(r'Any% Glitchless - Random Seed, 1.16+',na=False)
df = df[RSG16]
df['Date'] = df['Date'].str.replace(r'T12:00:00Z', '')
df['In-game-time'] = df['In-game-time'].str.replace(r'(in-game time)', '')
df['Game'] = df['Game'].str.replace(r'\n', '')


df.to_csv(r'D:\Foque\unb\proj\MCspeedrun\all_runs.csv',sep=";",index=False)











