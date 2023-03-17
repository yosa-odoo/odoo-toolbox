from datetime import date, datetime, timedelta


class WorkDay:

    def __init__(self, start, working_time, pauses):
        self.date = date.today()
        self.start_time = self.get_time_from_str(str(start))
        self.working_time = self.get_time_from_str(working_time)
        self.pauses = self._create_pauses(pauses)
        self.end_time = None

    @staticmethod
    def get_time_from_str(time_str):
        dict_format = {1: '%M', 2: '%H:%M'}
        key = len(time_str.split(':'))
        if key > 3:
            return None
        return datetime.strptime(time_str, dict_format[key])

    @staticmethod
    def _create_pauses(pauses):
        list_pauses = []
        for pause in pauses:
            list_pauses.append(PauseTime(pause))
        return list_pauses

    def compute_end_time(self):
        end_time = self.start_time + timedelta(hours=self.working_time.hour, minutes=self.working_time.minute)
        for pause in self.pauses:
            end_time += pause.duration_delta
        self.end_time = end_time

    def compute_overtime(self):
        return timedelta(hours=datetime.now().hour, minutes=datetime.now().minute) - \
               timedelta(hours=self.end_time.hour, minutes=self.end_time.minute)


class PauseTime:

    def __init__(self, pause):
        self.duration_time = WorkDay.get_time_from_str(str(pause))
        self.duration_delta = timedelta(hours=self.duration_time.hour, minutes=self.duration_time.minute)

    def __repr__(self):
        return f"PauseTime({self.duration_time.hour}:{self.duration_time.minute})"
