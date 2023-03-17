#!/usr/bin/env python
import fire

from models.workday import WorkDay
from utils.util import check_no_error, get_full_report

WORKING_TIME = '07:36'


def finish_time(start, *args):
    """
    Don't work too much

    Prints the time when you should stop working
        :param start: the time you started your day
        :param args: optional(s) duration of your break(s) + options (WIP)
    """
    pauses = list(args)
    if check_no_error(start, pauses):
        workday = WorkDay(start, WORKING_TIME, pauses)
        workday.compute_end_time()
        print(get_full_report(workday))


if __name__ == "__main__":
    fire.Fire(finish_time)
