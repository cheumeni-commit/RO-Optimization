
import pandas as pd
import json
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
from pandas.plotting import table

from config.directories import directories as dirs
from constants import *


def need_worker_per_day():
    manage = pd.read_excel(dirs.data_dir / c_SETTING, 
                            sheet_name='Manage',
                            index_col=0)
    return list(manage.need)


def available_worker():
    shift = pd.read_excel(dirs.data_dir / c_SETTING,
                            sheet_name='Shift',
                            index_col=0)
    # invert 0 and 1 in shift
    shift_rev = shift[shift.columns].apply(lambda r: 1-r[shift.columns],1)
    return shift_rev


def update_off_shift():
    try:
        with open(dirs.config_dir + c_OFF_SHIFT, 'r') as fp:
            off_shift = json.load(fp)
    except IOError:
        print("The file path does not exist")
        sys.exit(-1)

    print(off_shift)


def schedule_which_nurse(nurseWho = 0):
        
    '''
    nurseWho: nurse id
    table: Either the schedule dataframe or the linear programming solution
    inputType: if 'lp': use linear programming solution
                else: the dataframe
    '''
    # Get the data for scheduling nurse n:
    res = []
        
    for s in shifts:
        res.append(
            int(value(var[(nurseWho, s)]))
            )
    
    num_shift = len(daily_shift)
    res = np.array(res).reshape(len(res)/num_shift, num_shift).swapaxes(0, 1)
    
    col = ['week'+str(w) + '_' + str(d) for w in range(1, n + 1) for d in day]
    df_sch = pd.DataFrame(res, index = daily_shift, columns = col)
    
    return df_sch


def check_off_shift():
        
    # Check constraint:
    # 1) Nurse will only work on shift during a day
    # 2) Nurse who works on a late night shift will not work next day.
    for n in nurses:
        for s in shifts:
            if s%daily_shift_n == 0:
                if sum(value(var[(n,s+i)]) for i in range(daily_shift_n)) > 1:
                    print(2, n, s)
                    return False  # for day shift
            elif (s+1)%daily_shift_n == 0 and s < shifts[-1]:
                if sum(value(var[(n, s+i)]) for i in range(daily_shift_n+1)) > 1:
                    print(3, n, s)
                    return False

    # Check: maximum working shifts for a nurse
    for n in self.nurses:
        for i in range(self.n): 
            begin, end = self.c_LENGHT_OF_WEEK *self.daily_shift_n*i, self.c_LENGHT_OF_WEEK *self.daily_shift_n*(i+1)
            # each week: the nurse cannot work over 5 shifts.
            tmp = sum(value(self.var[(n,s)]) for s in self.shifts[begin:end]) 
            if tmp > self.nurse_max_shifts or tmp < 1:
                print(4, n, s, tmp)
                return False

    # check the maximum late night shifts for a nurse per week <= 1
    for n in self.nurses:
        for i in range(self.n):
            begin, end = self.c_LENGHT_OF_WEEK *self.daily_shift_n*i, self.c_LENGHT_OF_WEEK *self.daily_shift_n*(i+1)
            if sum(value(self.var[(n, s)]) for s in self.shifts[begin:end] if (s+1)%self.daily_shift_n == 0) > 1:
                print(5, n, s)
                return False

    # check the numbers of working nurses should be more than the required numbers of nurses.
    for s in self.shifts:
        try:
            if sum(value(self.var[(n,s)]) for n in self.nurses) < self.r[s]:
                print(6, n, s)
                return False
        except:
            print("len(shifts) should be equal to len(require_nurses)")
            sys.exit(-1)   

    return True
                     


def plot_table(df, daily_shift, fileDir, figSize = (4,2), saveFig = False, figTitle = 'nurse_scheduling'):
     
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
    #ax.xaxis.set_visible(False)  # hide the x axis
    #ax.yaxis.set_visible(False)
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

    # refresh the plot
    #plt.show()
    plt.close()


if __name__ == '__main__':

    print(need_worker_per_day())
