from datetime import datetime, timedelta
import re

import fire

WORK_HOURS = 7
WORK_MINUTES = 36

def get_body_message(start_time):
    return f"""
    -----             To the Bugfix Manager           -----\n
    ----- Report from The Assistant To Bugfix Manager -----\n
    \n
    Date: {datetime.today().strftime("%d %B %Y")}\n
    Starting of the day: {start_time.hour}:{start_time.minute}\n
    Length of a day: {WORK_HOURS} hours and {WORK_MINUTES}\n
    \n
    """

def finish_time(start, *pauses):
    """
    Don't work too much

    Prints the time when you should stop working
        :param start: the time you started your day - must be in the format "hh:mm"
        :param pauses: optional(s) duration of your break(s) - must be in the format "hh:mm" or "mm"
        :raises ValueError: If the format is not correct
    """
    start = str(start)
    if re.findall('[^0-9:]', start) or len(start.split(':')) != 2:
        raise ValueError("The start time should be in the format 'hh:mm'")

    start_time = datetime.strptime(start, '%H:%M')
    working_hours_delta = timedelta(hours=WORK_HOURS, minutes=WORK_MINUTES)
    finish = start_time + working_hours_delta
    message = get_body_message(start_time)

    for pause in pauses:
        pause = str(pause)
        if re.findall('[^0-9:]', pause) or len(pause.split(':')) > 2:
            raise ValueError("Must be in the format 'hh:mm' or 'mm'")

        pause_time = datetime.strptime(pause, '%H:%M') if ':' in pause else datetime.strptime(pause, '%M')
        pause_delta = timedelta(hours=pause_time.hour, minutes=pause_time.minute)
        finish += pause_delta
        message += f"Pause of {}"

    print(f"You should finish at max {finish.strftime('%H:%M')}")


if __name__ == "__main__":
    fire.Fire(finish_time)
