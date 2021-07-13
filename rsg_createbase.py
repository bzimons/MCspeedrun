import pandas as pd
from os import walk

_,_,files = next(walk('D:\\foque\\unb\\proj\\MCspeedrun\\players')) #

li = []
for filename in files:
    df = pd.read_csv('D:\\foque\\unb\\proj\\MCspeedrun\\players\\'+filename, index_col=None,
     header=0,sep=";",usecols=['Username','Game','In-game-time','Date'])
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.to_csv('D:\\foque\\unb\\proj\\MCspeedrun\\all_runs.csv',sep=";",index=False)










