import RPi.GPIO as GPIO
import time
import threading
from AlarmEMail import send_email
from datetime import datetime

"""
Code from
https://cdn-reichelt.de/documents/datenblatt/A300/SEN-HC-SR501-ANLEITUNG-23.09.2020.pdf
Pin-Setup:
    GPIO 7 Pin 7 Data
    Pin 9 GND
    Pin 4 5V
"""

class IR_Sensor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.Pin = 7
        GPIO.setup(self.Pin, GPIO.IN)
        self.activate = False

    def act_ir_sensor(self):
        self.activate = True
        self.email_send = False
        self.email_time = None
        if self.activate:
            self.i = threading.Thread(name='ir_alarm', target=self.ir_sensor)
            self.i.start()

    def stop_ir_sensor(self):
        self.activate = False
        
    def ir_sensor(self):
        print("Start", self.activate)
        # Zwischenvariablen
        movement = 0
        active = 0
        try:
            while self.activate:
                # Auslesen des GPIO4
                movement = GPIO.input(self.Pin)
                # Sensor hat neue Bewegung erkannt
                if movement == 1 and active == 0:
                    print("Movement, Email", self.email_send)
                    active = 1
                    if not self.email_send:
                        self.email_time = datetime.now()
                        self.email_send = True
                        send_email()
                    elif self.email_time != None:
                        # email already send, send another one if it was more than 5 mins ago
                        print((datetime.now() - self.email_time).total_seconds())
                        if (datetime.now() - self.email_time).total_seconds() > 300:
                            self.email_time = datetime.now()
                            send_email()
                # Sensor nimmt keine Bewegung mehr war nachdem ausgeloest wurde
                elif movement == 0 and active == 1:
                    print("No Movement")
                    active = 0
                time.sleep(0.1)
            print("Stop", self.activate)
        #Abbruchbedingung
        except KeyboardInterrupt:
            GPIO.cleanup()
