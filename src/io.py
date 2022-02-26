import logging

from config import directories as dirs
from constants import *

logger = logging.getLogger(__name__)

def save_schedule_tab(schedule):
    schedule.to_csv(dirs.data_dir / c_SCHEDULE, header = True)
    logger.info(f"Schedule saved")