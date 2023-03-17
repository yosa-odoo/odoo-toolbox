from datetime import datetime
import re
import sys


def check_no_error(start, pauses):
    # To avoid unnecessary long stack
    sys.tracebacklimit = 0

    def is_hour(hour):
        return 0 <= int(hour) < 24

    def is_minute(minute):
        return 0 <= int(minute) < 60

    # check start time
    start = str(start)
    start_split = start.split(':')
    if re.findall('[^0-9:]', start) or \
            len(start_split) != 2 or \
            not is_hour(start_split[0]) or\
            not is_minute(start_split[1]):
        raise ValueError("The start time should be in the format '%H:%M'\n"
                         "https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes")

    # check pause time
    for pause in pauses:
        pause = str(pause)
        pause_split = pause.split(':')
        if re.findall('[^0-9:]', pause) or \
                len(pause_split) > 2 or \
                not is_minute(pause_split[-1]) or \
                len(pause_split) == 2 and not is_hour(pause_split[0]):
            raise ValueError("Pause must be in the format '%H:%M' or '%M'.\n"
                             "https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes")
    # default stack limit
    sys.tracebacklimit = 1000
    return True


def get_full_report(workday):

    def get_pause_message(pauses):
        message = ""
        for pause in pauses:
            message += f"""
            - Pause of {int(pause.duration_delta.total_seconds() // 60)} minutes
            """
        return message

    main = f"""
    -------------------------------------------------------------
    -------------------------------------------------------------
    ------ Report from The Assistant To The Bugfix Manager ------    
    -------------------------------------------------------------
    -------------------------------------------------------------
    Date: {datetime.now().strftime("%d %B %Y %H:%M")}\n
    Starting of the day: {workday.start_time.strftime('%H:%M')}
    Duration of a working day: {workday.working_time.hour} hours and {workday.working_time.minute} minutes
    Pause(s):
    """

    footer = f"""
    -------------------  End of the day:{workday.end_time.strftime('%H:%M')}  -------------------
    ------------------- Overtime: {int(workday.compute_overtime().total_seconds() // 60)} minutes -------------------
    """

    return main + get_pause_message(workday.pauses) + footer
