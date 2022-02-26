import os
import json
import sys

import pandas as pd
import numpy as np
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import table

from pulp import *

from config.directories import directories as dirs
from constants import *
from features import need_worker_per_day, available_worker


class nurse:

    """
    workforce class for the scheduling problem
    """

    def __init__(self, daily_shift = 2, planning_length = 4,
                 total_nurses = None):


        # number of worker
        self.total_nurses = total_nurses

        # need worker per day
        self.nurse_per_shift = need_worker_per_day()

         # planning_length: 1 week, 2 week or 4 weeks
        self.numberWeek = len(self.nurse_per_shift) // planning_length

        # available worker
        self.available_worker = available_worker()
        #print(self.available_worker)
        # numbers of shift per day
        # for example: 
        # [day, night] = [0, 1]
        self.daily_shift = range(daily_shift)
        self.daily_shift_n = daily_shift

        # label each day from Monday to Friday:
        self.shift_name = [c_Week +str(w)+'_'+str(d)+'_'+str(i) \
                            for w in range(1, self.numberWeek+1) \
                            for d in c_WEEK for i in self.daily_shift]

        
        self.shifts = range((daily_shift * len(c_WEEK)* planning_length))

       
        self.r = []
        for p in self.nurse_per_shift:
            for _ in range(daily_shift):
                a = p//daily_shift
                self.r.append(a)

        # create workforce list and workforce_id tag:
        # workforce: label each workforce. Simply use integers to represent.
        self.nurses = range(self.total_nurses)
        self.nurses_id = [c_Workforce + str(i+1) for i in range(self.total_nurses)]

        # initialize a linear programming problem
        self.prob = LpProblem("Workforce scheduling", LpMinimize)


    def lp_problem(self):

        '''
        Use pulp to solve the constrained problem using linear programming(LP) algorithm. 
        1. Create LpVariables. Binary category in this case
        2. Add constraints in either equality or inequality conditions.
        3. Building objective using LpObjective. 
        '''
        
        # Creating the variables. 
        self.var = {(n, s): LpVariable("schedule_{}_{}".format(n, s), cat = "Binary") \
            for n in self.nurses for s in self.shifts}

        print(len(self.shifts), len(self.r))
        # add constraints: 
        for n in self.nurses:
            for s in self.shifts:
                if s%self.daily_shift_n == 0 and s < self.shifts[-4]:
                    # Nurses do not work in two consecutive shifts in a single day
                    self.prob.addConstraint(
                    sum(self.var[(n,s+i)] for i in self.daily_shift) <= 1  # for day shift
                    )
                    # Nurses do not work in 3 consecutive shifts night
                    self.prob.addConstraint(
                    sum(self.var[(n, s+self.daily_shift_n*i)] for i in range(3)) <= 1  # for day shift
                    )
                
                elif (s+1)%self.daily_shift_n == 0 and s < self.shifts[-5]:  # for late night shift
                    # Nurses do not work in 4 consecutive shifts night
                    self.prob.addConstraint(
                    sum(self.var[(n, s+self.daily_shift_n*i)] for i in range(4)) <= 1  # for night shift
                    )
                    # night shift. Do not forget to add condition that the last
                    # shift in the scheduling does not count.
                    self.prob.addConstraint(
                    sum(self.var[(n, s+i)] for i in range(self.daily_shift_n+1)) <= 1
                    )
  
        # add constraints
        # for each shift, the numbers of working nurses should be greater than
        # the required numbers of nurses
        print(len(self.shifts), len(self.r))
        for s in self.shifts:
            self.prob.addConstraint(
            sum(self.var[(n,s)] for n in self.nurses) >= self.r[s])

        self.prob.objective = sum(self.var[(n,s)] for n in self.nurses for s in self.shifts)   

        return self.prob
        

    def lp_solve(self, prob):
        # problem solver
        prob.solve()
        print("The status of solving the problem is: ")
        print(LpStatus[self.prob.status])


    def nurse_scheduling(self):
        # output the whole scheduling
        self.schedule = pd.DataFrame(data=None, index = self.nurses_id, columns = self.shift_name) 
        for k, v in self.var.items():
            n, s = k[0], k[1]
            self.schedule.iloc[n][s] = int(value(v))
        return self.schedule


if __name__ == '__main__':


    model = nurse(daily_shift = c_DAILY_SHIFT,         # There are three shifts a day: (day, evening, late night)
                  planning_length = c_PLANNING_LENGTH, # Scheduling length is 4 weeks.
                  total_nurses = c_NUMBER_WORKER
                  )

    prob = model.lp_problem()

    model.lp_solve(prob)

    schedule = model.nurse_scheduling()

    schedule.to_csv("/Users/jeanmichelcheumeni/RO-Optimization/data/"+ 'schedule.csv', header = True)

    print(schedule.head(15))