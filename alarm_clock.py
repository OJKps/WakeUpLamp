from datetime import datetime, date, timedelta
import time
import threading
from string import Template

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

class AlarmClock(object):
    def __init__(self, lamp):
        self.is_set = False
        self.input_time = None
        self.time_set_to = None
        self.lamp_obj = lamp
        self.sec_light_before_alarm = 40 * 60
        self.dimm_up_every_sec = 4 * 60 # shoulb be int dividable with sec_light_before_alarm to start dimm up at the sec_light_before_alarm time

    def alarm(self):
        # reset lamp to get correct step = 0 to start there when wake
        self.lamp_obj.reset()
        while self.is_set:
            time.sleep(1)
            current_time = datetime.now()
            now = current_time.strftime('%Y-%m-%d %H:%M:%S')
            #print(now, self.time_set_to)
            time_delta = self.time_set_to - current_time
            #print(time_delta)
            if time_delta.total_seconds() < self.sec_light_before_alarm:
                # start light wake up 40 minutes before alarm
                #print(time_delta.total_seconds())
                #print(round(time_delta.total_seconds()) % self.dimm_up_every_sec)
                if round(time_delta.total_seconds()) % self.dimm_up_every_sec == 0:
                    # every four minutes dimm light up
                    print("DIMM UP - WAKE UP")
                    self.lamp_obj.dimm_up()
            if time_delta.total_seconds() < 0:
                print("Time to Wake up")
                self.delete_alarm()
                #self.f.terminate()
                break

    def set_time(self, time_set_to):
        self.input_time = datetime.now()
        print(time_set_to)
        self.time_set_to = datetime.combine(date.today(), time_set_to)

        if (self.time_set_to - datetime.now()).total_seconds() < 0:
            self.time_set_to = self.time_set_to + timedelta(days=1)

        #self.time_set_to = time_set_to
        #self.time_set_to = datetime.strptime(time_set_to, '%Y-%m-%d %H:%M:%S')
        self.is_set = True
        self.f = threading.Thread(name='alarm', target=self.alarm)
        self.f.start()

    def delete_alarm(self):
        self.is_set = False
        #self.input_time = None
        #self.time_set_to = None

    def time_to_alarm(self):
        time_now = datetime.now()
        self.delta_time = (self.time_set_to - time_now)
        print(self.delta_time)
        print(time_now)
        return strfdelta(self.delta_time, "%H hours and %M minutes to go")