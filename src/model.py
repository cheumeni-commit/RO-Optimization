from src.constants import *
from src.scheduling import *


def training():

    model = Worker()
    prob = model.lp_problem()
    model.lp_solve(prob)
    schedule = model.nurse_scheduling()

    return schedule, model.daily_shift_n