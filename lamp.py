from lamp_signal import Lamp_Signaler
import time

class Lamp(Lamp_Signaler):
    """
    Object to give a signal to the IKEA --- lamp via the lamp_signal class.
    Controlles the lamp_signaler.
    Saves the birghtnes and lamp states.
    """
    def __init__(self):
        """
        lamp_step:
            Saves the brightness of the lamp
            0 -> lowest level
            ...
            8 -> highest level            
        """
        self.lamp_off = True
        self.lamp_step = "Please use reset in tab settings"
        self.max_step = 8
        self.min_step = 0
        super().__init__()
    
    def reset(self):
        self.turn_on()
        time.sleep(1)
        self.turn_off()

    def turn_on(self):
        self.lamp_off = False
        super().turn_on()
        
    def dimm_up_slow(self):
        self.lamp_off = False
        super().dimm_up_slow()

    def dimm_up(self):
        self.lamp_step += 1
        self.lamp_off = False
        if self.lamp_step <= self.max_step:
            # only dimm up when max step is not reached
            super().dimm_up()
        self.lamp_step = min(self.max_step, int(self.lamp_step))

    def dimm_down(self):
        self.lamp_step -= 1
        if self.lamp_step >= self.min_step:
            # only dimm down when min step is not reached
            # ToDo: you can not dimm if state is not set at the start
            super().dimm_down()
        self.lamp_step = max(self.min_step, int(self.lamp_step))

    def turn_off_fast(self):
        self.lamp_off = True
        super().turn_off_fast()

    def turn_off(self):
        self.lamp_off = True
        self.lamp_step = 0
        super().turn_off()
        
