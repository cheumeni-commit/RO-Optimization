import logging
import pandas as pd

from src.config.directories import directories as dirs
from src.constants import *

logger = logging.getLogger(__name__)


def save_schedule_tab(schedule):
    schedule.to_csv(dirs.data_dir / c_SCHEDULE, header = True)
    logger.info(f"Schedule saved")


def read_setting(var):
    manage = pd.read_excel(dirs.data_dir / c_SETTING, 
                            sheet_name=var,
                            index_col=0)
    return manage