from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from selenium import webdriver
from datetime import datetime
from selenium.webdriver import ActionChains


def remove_rep(string_name):
    n = int(len(string_name)/2)
    letters = list(string_name)
    name = ''.join(letters[0:n])
    return(name)

browser = webdriver.Firefox(executable_path="D:\\foque\\unb\\proj\\driver\\geckodriver.exe")
url = ('https://www.speedrun.com/mcce#Filtered_Seed_Glitchless')
#/html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/button
# /html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/ul/li[8]/a
# /html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/ul/li[8]/ul/a[2]
#/html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/ul/li[8]/a
browser.get(url)

try:
    browser.find_element_by_xpath('''/html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/button''').click()
    sleep(5)
    menu = browser.find_element_by_xpath("/html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/ul/li[8]/a")
    hidden_submenu = browser.find_element_by_xpath('''/html/body/div[8]/main/div/div[3]/div/form/div/div[1]/div[2]/div[1]/ul/li[8]/ul/a[2]''')
    ActionChains(browser).move_to_element(menu).click(hidden_submenu).perform()
    sleep(8)
except:
    pass



respData = browser.page_source
browser.close()
soup = BeautifulSoup(respData, 'html.parser')

table = soup.find( "table") 
table_str = str(table) 
df  = pd.read_html(table_str)[0] 

df = df.drop(['Rank','Version', 'Unnamed: 12', 'Unnamed: 10', 'Unnamed: 11'], axis=1)

Player = df['Players'].tolist()
Player_new = [remove_rep(i) for i in Player]
df['Player'] = Player_new

all_date=[]
for i in table.findAll('time',class_="short circa"):
    if i.has_attr('datetime'):
        date = i['datetime']
        all_date.append(date)

df['Date'] = all_date
df['Date'] = df['Date'].str.replace(r'T12:00:00Z', '')
print(df.head(10))

# glinks=[]
# for a in table.find_all('a', href=True):
#     glinks.append('https://www.speedrun.com' + a['href']) 

# df.loc[:,'userlink'] = pd.Series(glinks[2:])
# df

extract = datetime.today().strftime('%y-%m-%d') 
day = 'board_'+extract+'.csv'

df_top50 = df[:50] #keep top 50
print(df_top50)
df.to_csv(r'D:\Foque\unb\proj\MCspeedrun\board\\fsg_'+day,index=False,sep=",") 

