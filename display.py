from PIL import Image, ImageDraw, ImageFont
#import matplotlib.pyplot as plt
from datetime import datetime
import time
import threading
#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED

class Display(object):
    def __init__(self):
        print("INIT DISPLAY")
        try:
            OLED.Device_Init()
        except:
            print("ERROR INIT DISPLAY")
        self.time_displaying = 0
        self.max_time_display = 30
        self.refresh_rate = 7 # in seconds
        self.alarm_set = False
        self.alarm_set_to = None # dattime
    
    def clear_display(self):
        OLED.Clear_Screen()
        self.time_displaying = 0
    
    def display_image(self, path):
        image = Image.open(path)
        OLED.Display_Image(image)
        self.r = threading.Thread(name='timer_display_image', target=self.timer_clear_display)
        self.r.start()
    
    def display_clock(self, alarm_set, alarm_set_to):
        self.alarm_set = alarm_set
        self.alarm_set_to = alarm_set_to
        self.draw_clock()
        if self.time_displaying == 0:
            self.t = threading.Thread(name='timer_display', target=self.timer_clear_display)
            self.t.start()
    
    def change_display(self):
        # trigger and wait for clearing display
        if self.time_displaying != 0:
            # something is beging displayed
            self.time_displaying = self.max_time_display
            time.sleep(1.1)
            self.time_displaying = 0
    
    def timer_clear_display(self):
        while self.time_displaying < self.max_time_display:
            time.sleep(1)
            self.time_displaying += 1
            if (self.time_displaying % self.refresh_rate) == 0:
                # refresh
                self.draw_clock()
        self.clear_display()
        self.time_displaying = 0
        
    def draw_clock(self): # alarm
        try:
            image = Image.new("RGB", (128, 128), 0)  # grayscale (luminance)
            draw = ImageDraw.Draw(image)

            n = datetime.now()
            t_n = n.strftime("%H:%M")
            d_n = n.strftime("%d-%m-%Y")

            w, h = draw.textsize(t_n)
            draw.text(((127 - w) / 2, (((127 - h) / 2) - (5))), t_n, fill="White")
            w, h = draw.textsize(d_n)
            draw.text(((127 - w) / 2, (((127 - h) / 2) + (5))), d_n, fill="White")
            
            if self.alarm_set:
                alarm_txt = self.alarm_set_to.strftime("%H:%M")
                w, h = draw.textsize(alarm_txt)
                draw.text(((127 - w) / 2, (((127 - h) / 2) + (15))), alarm_txt, fill="Red")

                draw.ellipse([(((127 / 2) - (w / 2) - 10), (((127 - h) / 2) + 16)), (((127 / 2) - (w / 2) - 3), (((127 - h) / 2) + 16 + 7))], fill="Red")
                draw.ellipse([(((127 / 2) + (w / 2) + 1), (((127 - h) / 2) + 16)), (((127 / 2) + (w / 2) + 8), (((127 - h) / 2) + 16 + 7))], fill="Red")

            # annotate hours
            hour = "12"
            w, h = draw.textsize(hour)
            draw.text(((127 - w) / 2, 10), hour, fill="White")
            hour = "3"
            w, h = draw.textsize(hour)
            draw.text(((127 - w - 10), ((127 - h) / 2)), hour, fill="White")
            hour = "6"
            w, h = draw.textsize(hour)
            draw.text((((127 - w) / 2), (127 - h - 10)), hour, fill="White")
            hour = "9"
            w, h = draw.textsize(hour)
            draw.text((10, (127 - h) / 2), hour, fill="White")

            if n.hour < 12:
                hour = n.hour + n.minute / 60.
            else:
                hour = (n.hour - 12) + n.minute / 60.

            # 12h - -90 270
            # 9h - -90 180
            # 6h - -90 90
            # 3h - -90 0
            # 0h - -90 -90

            # from -90 to 270
            # 360 / 12 =  30

            # full degree hour if start=0 is at the top
            hour_degree = 30 * hour
            hour_degree -= 90

            draw.arc((0, 0, 127, 127), start=-90, end=hour_degree, fill=(255, 255, 0), width=3)

            # 360 / 60 = 6 degree per minute
            min_degree = 6 * n.minute
            min_degree -= 90

            draw.arc((5, 5, 122, 122), start=-90, end=min_degree, fill=(255, 0, 0), width=3)

            #plt.imshow(image)
            #plt.show()
            OLED.Display_Image(image)
        except:
            print("ERROR, CREATING A CLOCK")
            
        
