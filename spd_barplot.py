from numpy.core import numeric
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
from datetime import date, timedelta,datetime
import bar_chart_race2 as bcr
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import re
from matplotlib.animation import FuncAnimation
from matplotlib import cm
from itertools import compress

# plt.rcParams['animation.ffmpeg_path'] = 'C:\\FFmpeg\\bin\\ffmpeg.exe'


df = pd.read_csv(r'D:\Foque\unb\proj\MCspeedrun\all_runs.csv',sep=";",usecols=['Username','Game','In-game-time','Date'])
# df = df.sample(100,random_state=2)
bol=df['Game'].astype(str).str.startswith(r'Any% Glitchless - Random Seed, 1.16+')
df = df[bol]
df = df[['Username','In-game-time','Date']]
player = df['Username']
# print(df.head(20))

data= df['Date']
DATE = [datetime.strptime(x,'%Y-%m-%d').date() for x in data] # '%d/%m/%Y'
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
ts = [(t.hour * 3600 + t.minute * 60 + t.second + (t.microsecond)*(10**-6)) for t in TIME] # 1/ inverse, to plot the lower time on top or chart
df['In-game-time']=ts

# ONLY SUB20

bol=[i.hour==0 and i.minute<20 for i in TIME]
df = df[bol]
TIME = list(compress(TIME, bol))
DATE=df['Date']

d1 = min(DATE) #lower date
d2 = max(DATE) 

# list containing all of the dates
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
dd =  [x for x in dd if x not in DATE]
dd = pd.DataFrame({'Date':dd})
df = dd.append(df, ignore_index = True)
df['Username'] = df['Username'].fillna('dummy')
df['In-game-time'] = df['In-game-time'].fillna(0)
# df= df.sort_values(by=['Date'])
# print(df.head(10))
# print(df.tail(10))

#df = df.pivot_table(index='Date',columns='Username',values='In-game-time',aggfunc=min, dropna=False) 
df = df.pivot_table(index=['Date'], columns=['Username'],values='In-game-time')
# df = df.pivot(index=['Date'], columns=['Username'],values='In-game-time')
# df = df.set_index('Username', append=True).groupby(level=[0, 1])['In-game-time'].sum(min_count=1).unstack(-1)
df = df.drop(columns=['dummy'])
# print(df.head(10))
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

# with pd.option_context('display.max_rows', None): 
#     print(df[['Funderful_TV','realbenex','TheeSizzler']])


plt.rcParams['animation.ffmpeg_path'] = 'C:\\FFmpeg\\bin\\ffmpeg.exe'
fig, ax = plt.subplots(figsize=(7, 4.5)) # 6, 3.5
ax.set_facecolor((0, 0, 0, 1))
fig.set_facecolor((0, 0, 0, 1)) # add final
ax.set_ylim(0,11) # wrong, but works
ax.set_yticks(np.arange(10))
plt.xticks([])
#plt.figtext(0.7, 0.01, "github.com/bzimons", ha="left", fontsize=12,color='w')
plt.title('History of sub20 1.16+ RSG Minecraft Speedrun ',color='w')


bcr.bar_chart_race(
    df=df,
    filename='D:\\foque\\unb\\proj\\MCspeedrun\\barrace.mp4',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.90,
    period_label={'x': .95, 'y': -.05, 'ha': 'right', 'va': 'center','color':'w','family' : 'Franklin Gothic Medium','size': 12}, # date posix
    # period_fmt='%B, %d, %Y',
    period_summary_func=lambda v, r: {'x': .99, 'y':  1,'s': f'',
    'ha': 'right', 'size': 8, 'family' : 'Franklin Gothic Medium'},
    #perpendicular_bar_func='median',
    period_length=500,
    figsize=(5, 3),
    dpi=300,
    cmap= cm.get_cmap('jet', 50),
    title='kd o titulo',
    title_size='',
    bar_label_size=9,
    tick_label_size=5,
    shared_fontdict={'family' : 'Franklin Gothic Medium', 'color' : '.1'},
    scale='linear',
    writer='ffmpeg',
    fig=fig,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)  



