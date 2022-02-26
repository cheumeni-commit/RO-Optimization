import json
import sys
import os
import matplotlib.pyplot as plt
from pandas.plotting import table

from src.in_out import read_setting
from src.config.directories import directories as dirs
from src.constants import *



def need_worker_per_day():
    manage = read_setting(c_MANAGE)
    return list(manage.need)


def available_worker():
    shift = read_setting(c_SHIFT) 
    # invert 0 and 1 in shift
    shift_rev = shift[shift.columns].apply(lambda r: 1-r[shift.columns],1)
    return shift_rev


def pair_avoid(var):
    member = read_setting(c_MEMBER).T
    avoid_list = member[member[var].isin([1])].index # var :'pairs1'
    return avoid_list


def indice_binaire(v):
    index = [i for i,e in enumerate(v) if e==1]
    return index


def update_off_shift():
    try:
        with open(dirs.config_dir + c_OFF_SHIFT, 'r') as fp:
            off_shift = json.load(fp)
    except IOError:
        print("The file path does not exist")
        sys.exit(-1)

    print(off_shift)

                    
def plot_table(df, daily_shift, fileDir, figSize = (4,2), saveFig = False, figTitle = c_WORKER_SCHEDULE):
     
    # visulize the schedule  
    #colors = df.applymap(lambda i, j: 'lightgray' if df.iloc[i,j] == 0 else 'lightcoral')
    colors = [['lightgray'] * df.shape[1] for _ in range(df.shape[0])]
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i][j]:
                colors[i][j] = 'lightcoral'
            elif (j+1)%daily_shift == 0:
                colors[i][j] = 'orange'
            else:
                colors[i][j] = 'lightgray'

    fig = plt.figure(figsize=figSize)

    ax = plt.subplot(2, 1, 1, frame_on = True)  # no visible frame
    ax.axis('off')

    tb1 = table(ax, df,
                loc='center',
                cellLoc='center',
                cellColours=colors,
                fontsize=14
          )

    if saveFig == True:
        print(fileDir)
        if not os.path.isdir(fileDir):
            os.mkdir(fileDir)
        plt.savefig(fileDir + figTitle +'.png', bbox_inches='tight', dpi = 150)

    #plt.show()
    plt.close()