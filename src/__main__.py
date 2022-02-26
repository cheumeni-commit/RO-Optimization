

from model import training
from io import save_schedule_tab


if __name__ == '__main__':
    schedule = training()
    save_schedule_tab(schedule)