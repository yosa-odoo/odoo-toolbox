from datetime import datetime, timedelta
import re

import fire

WORK_HOURS = 7
WORK_MINUTES = 36


def get_body_message(start_time):
    return f"""
    -------------------------------------------------------------
    -------------------------------------------------------------
    ------              To the Bugfix Manager              ------
    ------ Report from The Assistant To The Bugfix Manager ------
    -------------------------------------------------------------
    -------------------------------------------------------------
    Date: {datetime.now().strftime("%d %B %Y %H:%M")}\n
    Starting of the day: {start_time.hour}:{start_time.minute}
    Length of a working day: {WORK_HOURS} hours and {WORK_MINUTES} minutes\n
    """


def add_pauses(end_of_day, pauses, message):
    for pause in pauses:
        pause = str(pause)
        if re.findall('[^0-9:]', pause) or len(pause.split(':')) > 2:
            raise ValueError("Must be in the format 'hh:mm' or 'mm'")

        pause_time = datetime.strptime(pause, '%H:%M') if ':' in pause else datetime.strptime(pause, '%M')
        pause_delta = timedelta(hours=pause_time.hour, minutes=pause_time.minute)
        end_of_day += pause_delta
        message += f"""
        - Pause of {int(pause_delta.total_seconds() // 60)} minutes
        """
    return end_of_day, message


def end_of_day_message(body_message, end_of_day):
    overtime = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute) -\
               timedelta(hours=end_of_day.hour, minutes=end_of_day.minute)
    return f"""
    {body_message}\n
    ------------------- End of the day: {end_of_day.strftime('%H:%M')} -------------------
    ------------------- Overtime: {int(overtime.total_seconds() // 60)} minutes -------------------
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

    end_of_day = start_time + working_hours_delta
    body_message = get_body_message(start_time)
    end_of_day, body_message = add_pauses(end_of_day=end_of_day, message=body_message, pauses=pauses)

    print(end_of_day_message(body_message, end_of_day))


if __name__ == "__main__":
    fire.Fire(finish_time)
