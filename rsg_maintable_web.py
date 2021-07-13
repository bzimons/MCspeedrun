from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from datetime import datetime

def remove_rep(string_name):
    n = int(len(string_name)/2)
    letters = list(string_name)
    name = ''.join(letters[0:n])
    return(name)

browser = webdriver.Firefox(executable_path="D:\\foque\\unb\\proj\\driver\\geckodriver.exe")
url = ('https://www.speedrun.com/mc#Any_Glitchless')
browser.get(url)
respData = browser.page_source
browser.quit()
soup = BeautifulSoup(respData, 'html.parser')

table = soup.find( "table") 
table_str = str(table) 
df  = pd.read_html(table_str)[0] 
df = df.drop(['Rank','Version', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11'], axis=1)

Player = df['Player'].tolist()
Player_new = [remove_rep(i) for i in Player]
df['Player'] = Player_new

glinks=[]
for a in table.find_all('a', href=True):
    glinks.append('https://www.speedrun.com' + a['href']) 

df.loc[:,'userlink'] = pd.Series(glinks[2:])
df

extract = datetime.today().strftime('%y-%m-%d') 
day = 'board_'+extract+'.csv'

df_top50 = df[:50] #keep top 50
print(df_top50)
df.to_csv(r'D:\Foque\unb\proj\MCspeedrun\board\\'+day,index=False,sep=",") 

