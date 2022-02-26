import logging

from src.constants import *
from src.config.directories import directories as dirs
from src.features import plot_table
from src.in_out import save_schedule_tab
from src.model import training

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # run optimization
    schedule = training()
    # plot and save png table
    plot_table(schedule, c_DAILY_SHIFT, fileDir = "/Users/jeanmichelcheumeni/RO-Optimization/data/", figSize = (10, 4), saveFig = True)
    # save .csv table
    save_schedule_tab(schedule)

    logger.info(schedule.head(15))