import RPi.GPIO as GPIO
import time


class Lamp_Signaler(object):
    """
    Object to give a signal to the IKEA --- lamp via the dimmer controller.
    """
    def __init__(self):
        """
        Please call clean_up() when finished
        GPIO 16 is connected to the relay which controlles S1 (ON, BRIGHTER) to RELAY 1
        GPIO 18 is connected to the relay which controlles S2 (OFF, DARKER) to RELAY 3
        """
        print("created object Lamp Signaler")
        GPIO.setmode(GPIO.BOARD)
        
        self.S1_ON = 16
        self.S2_OFF = 18
        
        GPIO.setup(self.S1_ON, GPIO.OUT) # S1 ON/BRIGHTER
        GPIO.setup(self.S2_OFF, GPIO.OUT) # S2 OFF/DARKER
        
        # True and False are defined by the Relay
        self.OFF = True # define True for GPIO pins as OFF
        self.ON = False # define False for GPIO pins as ON
        
        try:
            # Turn OFF both relays
            GPIO.output(self.S1_ON, self.OFF) # -> S1 OFF
            GPIO.output(self.S2_OFF, self.OFF) # -> S2 OFF
        except:
            print("ERROR: In CLASS Lamp_Signaler: method init failed")
            GPIO.cleanup()
        
    def switch_on_relay_fast(self, relay):
        """
        Give a short signal to relay (S1 or S2)
        When S1 (ON):
            - lamp turned off: turn on
            - lamp turned on: nothing
        When S2 (OFF):
            - lamp turned off: nothing
            - lamp turned on: turn off
        param relay: S1 or S2
        """
        try:
            time.sleep(1)
            GPIO.output(relay, self.ON) # -> relay ON
            relay_name = str(relay)
            message_out = "Relay " + relay_name + "switched ON - FAST"
            print(message_out)
            time.sleep(0.6)
            GPIO.output(relay, self.OFF) # -> relay OFF
            message_out = "Relay " + relay_name + "switched OFF"
            print(message_out)
        except:
            GPIO.cleanup()
            print("ERROR: In CLASS Lamp_Signaler: method switch_relay_fast failed with relay")
    
    def switch_on_relay_slow(self, relay):
        """
        Give a long (5sec) signal to relay (S1 or S2)
        When S1 (ON):
            - lamp turned off: turn on and gets brigther
            - lamp turned on: gets brigther, too full brightness
        When S2 (OFF):
            - lamp turned off: nothing
            - lamp turned on: gets darker (DOES NOT TURN OFF)
        param relay: S1 or S2
        """
        try:
            time.sleep(1)
            GPIO.output(relay, self.ON) # -> relay ON
            relay_name = str(relay)
            message_out = "Relay " + relay_name + "switched ON - SLOW"
            print(message_out)
            time.sleep(5)
            GPIO.output(relay, self.OFF) # -> relay OFF
            message_out = "Relay " + relay_name + "switched OFF"
            print(message_out)
        except:
            GPIO.cleanup()
            print("ERROR: In CLASS Lamp_Signaler: method switch_on_relay_slow failed with relay")
            
    def switch_on_relay_step(self, relay):
        """
        Give a step (1sec) signal to relay (S1 or S2)
        When S1 (ON):
            - lamp turned off: turn on and gets brigther
            - lamp turned on: gets brigther, too full brightness
        When S2 (OFF):
            - lamp turned off: nothing
            - lamp turned on: gets darker (DOES NOT TURN OFF)
        param relay: S1 or S2
        """
        try:
            time.sleep(1)
            GPIO.output(relay, self.ON) # -> relay ON
            relay_name = str(relay)
            message_out = "Relay " + relay_name + "switched ON - SLOW"
            print(message_out)
            time.sleep(1.1)
            GPIO.output(relay, self.OFF) # -> relay OFF
            message_out = "Relay " + relay_name + "switched OFF"
            print(message_out)
        except:
            GPIO.cleanup()
            print("ERROR: In CLASS Lamp_Signaler: method switch_on_relay_slow failed with relay")
    
    def turn_on(self):
        """
        Give a short signal to turn on the lamp
        """
        print("Signal to lamp to turn ON")
        self.switch_on_relay_fast(self.S1_ON) # -> S1 relay ON for 0.5 sec than OFF
        print("Lamp should be turned ON")
        
    def dimm_up_slow(self):
        """
        Give a short signal to turn on the lamp
        Also turns the lamp ON when OFF
        """
        print("Signal to lamp to turn ON and DIMM UP")
        self.switch_on_relay_slow(self.S1_ON)
        print("Lamp should be turned ON andd DIMMED UP")
        
        
    def dimm_up(self):
        """
        Give a short signal to dimm up the lamp
        Also turns the lamp ON when OFF
        """
        print("Signal to lamp to DIMM UP")
        self.switch_on_relay_step(self.S1_ON) # -> S1 relay ON for 0.5 sec than OFF
        print("Lamp should one step BRIGHTER")
        
    def dimm_down(self):
        """
        Give a short signal to dimm down the lamp
        """
        print("Signal to lamp to DIMM DOWN")
        self.switch_on_relay_step(self.S2_OFF) # -> S2 relay ON for 0.5 sec than OFF
        print("Lamp should one step DARKER") 
        
    def turn_off_fast(self):
        """
        Give a short signal to off on the lamp - FAST
        """
        print("Signal to lamp to turn OFF - FAST")
        self.switch_on_relay_fast(self.S2_OFF) # -> S2 realy ON for 0.5 sec than OFF
        print("Lamp should be turned OFF")
    
    def turn_off(self):
        """
        Give a short signal to off on the lamp - SLOW
        """
        print("Signal to lamp to turn OFF - SLOW")
        self.switch_on_relay_slow(self.S2_OFF) # -> S2 realy ON for 5 sec than OFF
        print("Lamp should be dark")
        self.switch_on_relay_fast(self.S2_OFF) # -> S2 realy ON for 0.5 sec than OFF
        print("Lamp should be turned OFF")
    
    def clean_up(self):
        GPIO.cleanup()
        
        