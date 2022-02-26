import pandas as pd

from pulp import *

from src.constants import *
from src.features import need_worker_per_day
from src.features import available_worker
from src.features import indice_binaire
from src.features import pair_avoid


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

        # numbers of shift per day
        # for example: 
        # [day, night] = [0, 1]
        self.daily_shift = range(daily_shift)
        self.daily_shift_n = daily_shift

        # label each day from Monday to Friday:
        self.shift_name = [c_Week +str(w)+'_'+str(d)+'_'+str(i) \
                            for w in range(1, self.numberWeek) \
                            for d in c_WEEK for i in self.daily_shift]

        
        self.shifts = range((daily_shift * len(c_WEEK)* planning_length))
        # number of worker per shift
        self.worker_per_shift = [p//daily_shift for p in self.nurse_per_shift for _ in range(daily_shift)]

        # create workforce list and workforce_id tag:
        # workforce: label each workforce. Simply use integers to represent.
        self.nurses = range(self.total_nurses)
        self.nurses_id = [c_Workforce + str(i+1) for i in range(self.total_nurses)]

        # rename column of dataset of available
        self.dictionary = {k:v for k,v in zip(self.available_worker.columns, self.nurses_id)}
        print(self.dictionary)
        self.available_worker.columns = self.nurses_id

        self.off_shift_worker = {k:indice_binaire(self.available_worker[k]) \
                                for k in self.available_worker.columns}
        # association table
        self.association_index_workforce = {k:v for k, v in enumerate(self.nurses_id)}
        self.association_workforce_index = {v:k for k, v in enumerate(self.nurses_id)}

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

        print(len(self.shifts), len(self.worker_per_shift))
        # add constraints: 
        for n in self.nurses:
            for s in self.shifts:
                if s%self.daily_shift_n == 0 and s < self.shifts[-4]:
                    # worker do not work in two consecutive shifts in a single day
                    self.prob.addConstraint(
                    sum(self.var[(n,s+i)] for i in self.daily_shift) <= 1  # for day shift
                    )
                    # worker do not work in 3 consecutive shifts night
                    self.prob.addConstraint(
                    sum(self.var[(n, s+self.daily_shift_n*i)] for i in range(3)) <= 1  # for day shift
                    )
                
                elif (s+1)%self.daily_shift_n == 0 and s < self.shifts[-5]:  # for late night shift
                    # worker do not work in 4 consecutive shifts night
                    self.prob.addConstraint(
                    sum(self.var[(n, s+self.daily_shift_n*i)] for i in range(4)) <= 1  # for night shift
                    )
                    # night shift. Do not forget to add condition that the last
                    # shift in the scheduling does not count.
                    self.prob.addConstraint(
                    sum(self.var[(n, s+i)] for i in range(self.daily_shift_n+1)) <= 1
                    )

        # add constraints
        # day off for worker
        for n in self.nurses:
            for s in self.shifts:
                if s in self.off_shift_worker.get(self.association_index_workforce.get(n)):
                    self.prob.addConstraint(
                    self.var[(n, s)] == 0
                    )
        # add constraints
        # pair to avoid
        pair_1, pair_2 = pair_avoid(c_PAIR_1), pair_avoid(c_PAIR_2)
        worker1 = [self.association_workforce_index.get(self.dictionary.get(i)) for i in pair_1]
        worker2 = [self.association_workforce_index.get(self.dictionary.get(i)) for i in pair_2]

        for s in self.shifts:
            self.prob.addConstraint(
            sum(self.var[(n, s)] for n in worker1) <= 1  
            )
            self.prob.addConstraint(
            sum(self.var[(n, s)] for n in worker2) <= 1  
            )

        # add constraints
        # skilled member
        ver_senior = pair_avoid(c_SENIOR)
        senior = [self.association_workforce_index.get(self.dictionary.get(i)) for i in ver_senior]

        for s in self.shifts:
            self.prob.addConstraint(
            sum(self.var[(n, s)] for n in senior) <= 2  
            )
  
        # add constraints
        # for each shift, the numbers of working worker should be greater than
        # the required numbers of worker
        print(len(self.shifts), len(self.worker_per_shift))
        for s in self.shifts:
            self.prob.addConstraint(
            sum(self.var[(n,s)] for n in self.nurses) >= self.worker_per_shift[s])

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