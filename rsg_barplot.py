from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
from datetime import timedelta,datetime
import bar_chart_race2 as bcr
import matplotlib.pyplot as plt
import re
from matplotlib import cm
from itertools import compress

# plt.rcParams['animation.ffmpeg_path'] = 'C:\\FFmpeg\\bin\\ffmpeg.exe'


df = pd.read_csv(r'D:\Foque\unb\proj\MCspeedrun\all_runs.csv',sep=";",usecols=['Username','Game','In-game-time','Date'])
# df = df.sample(100,random_state=2)
bol=df['Game'].astype(str).str.startswith(r'Any% Glitchless - Random Seed, 1.16+')
df = df[bol]
df = df[['Username','In-game-time','Date']]
player = df['Username']


ddate= df['Date']
DATE = [datetime.strptime(x,'%Y-%m-%d').date() for x in ddate] # '%d/%m/%Y'
df['Date']=DATE

TIME= df['In-game-time']
TIME = [re.sub('(\(|\))','',x) for x in TIME]
newTIME=[]
for i in TIME:
    if('h' not in i):
        i= '0h' + i
    if(len(i)<12):
        i = i + '000ms'
    i = re.sub(' ','',i)
    newTIME.append(i)

TIME = [datetime.strptime(x,"%Hh%Mm%Ss%fms").time() for x in newTIME]
ts = [(t.hour * 3600 + t.minute * 60 + t.second + (t.microsecond)*(10**-6)) for t in TIME] 
df['In-game-time']=ts



# ONLY SUB20
bol=[i.hour==0 and i.minute<20 for i in TIME]
df = df[bol]
TIME = list(compress(TIME, bol))
DATE=df['Date']

d1 = min(DATE) 
d2 = max(DATE) 

# list containing all of the dates
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
dd =  [x for x in dd if x not in DATE]
dd = pd.DataFrame({'Date':dd})
df = dd.append(df, ignore_index = True)
df['Username'] = df['Username'].fillna('dummy')
df['In-game-time'] = df['In-game-time'].fillna(0)



df = df.pivot_table(index=['Date'], columns=['Username'],values='In-game-time')
df = df.drop(columns=['dummy'])

df = pd.DataFrame(df.to_records())#

players = list(df.columns)[1:]

for j in players:
    valor=NaN
    for i in range(0,len(df)):
        bolean =  df[j].isnull()[i]
        if(bolean):
            df[j][i] = valor
        else:
            valor = df[j][i]

df = df.rename(columns={"Date": "date"})
df.index = df['date']
df =df.drop(columns=['date'])
df.index = pd.to_datetime(df.index)

# with pd.option_context('display.max_rows', None): 
#     print(df[['Funderful_TV','realbenex','TheeSizzler']])


plt.rcParams['animation.ffmpeg_path'] = 'C:\\FFmpeg\\bin\\ffmpeg.exe'
fig, ax = plt.subplots(figsize=(7, 4.5)) # 6, 3.5
ax.set_facecolor((0, 0, 0, 1))
fig.set_facecolor((0, 0, 0, 1)) 
ax.set_ylim(0,11)
ax.set_yticks(np.arange(10))
plt.xticks([])
plt.title('Top 10 sub20 1.16+ RSG Minecraft Speedrun ',color='w')


bcr.bar_chart_race(
    df=df,
    filename='D:\\foque\\unb\\proj\\MCspeedrun\\RSG_barrace.mp4',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.90,
    period_label={'x': .95, 'y': -.05, 'ha': 'right', 'va': 'center','color':'w','family' : 'Franklin Gothic Medium','size': 15}, # date posix
    period_summary_func=lambda v, r: {'x': .99, 'y':  1,'s': f'',
    'ha': 'right', 'size': 8, 'family' : 'Franklin Gothic Medium'},
    period_length=500,
    figsize=(5, 3),
    dpi=300,
    cmap= cm.get_cmap('jet', 50),
    title='',
    title_size='',
    bar_label_size=9,
    tick_label_size=5,
    shared_fontdict={'family' : 'Franklin Gothic Medium', 'color' : '.1'},
    scale='linear',
    writer='ffmpeg',
    fig=fig,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)  



