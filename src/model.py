

from constants import *
from workforce_scheduling import *



def training():

    model = nurse(daily_shift = c_DAILY_SHIFT,                   # There are three shifts a day: (day, evening, late night)
                    planning_length = c_PLANNING_LENGTH,             # Scheduling length is 4 weeks.
                    total_nurses = c_NUMBER_WORKER
                    )

    prob = model.lp_problem()
    model.lp_solve(prob)
    schedule = model.nurse_scheduling()
    return schedule