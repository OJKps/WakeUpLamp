# WakeUpLamp
This is a simple WakeUpLamp to build yourself. The WakeUpLamp is made as simple as possible and safe to build and operate,
there is no need to work with high current. 
The core idea is to utilize the provided features of the IKEA TRÅDFRI lamp and its remote control. 
The remote control is switched via a RaspberryPi. 
This means that the lamp can be placed independently of the RaspberryPi and you do not have to work with large currents. 
To control the lamp, the Raspberry hosts a local website where you can fully control the lamp, set an alarm and much more.
Please note that the documentation will be updated in future, I will also upload a full instruction for the build.

Author: Oliver Becker

See the examples:

## Hardware
* RaspberryPi 3 B+ (bottom)
* IKEA TRÅDFRI lamp control (upper left)
* IKEA picture frame
* Relay (upper right - 2 Channels needed)
* GY-BME280 Sensor - temperature (top)
* HC-SR501 PIR Sensor - infrared (top)
* 1.5" 128x128 OLED Display Modul, RGB (middle)

<div class="row">
  <div class="column">
    <img alt="original" src="/Example_Images_WakeUpLamp/Hardware_WakeUpLamp2.jpeg" width="300px" />
  </div>
  <div class="column">
    <img alt="original" src="/Example_Images_WakeUpLamp/Hardware_WakeUpLamp.PNG" width="300px" />
  </div>
</div>

Everything is fitted into a inexpensive picture frame. Therefore a wooden backboard is created on which the Pi, Relay and the lamp controller a placed. The acrylic glass is fixed on top of the frame and hold by simple, sliding frame-holders. Everytime the website is used the display shows time and current alarm.

## Hosted Website to control the WakeUpLamp

### Dashboard
<img alt="original" src="/Example_Images_WakeUpLamp/Dashboard_WakeUpLamp.PNG" height="500px" />

Control the lamp and monitor. Multiple users can use the website, each user has its own login and entity in a SQLAlchemy database.

### Work Mode
<img alt="original" src="/Example_Images_WakeUpLamp/WorkMode_WakeUpLamp.PNG" height="500px" />

Track your working time
### Track Expenses
<img alt="original" src="/Example_Images_WakeUpLamp/ModeMode_WakeUPLamp.PNG" height="500px" />

Monitor expenses over multiple users
### Backpain Monitor
<img alt="original" src="/Example_Images_WakeUpLamp/BackPainMonitor_WakeUpLamp.PNG" height="500px" />

Plot your backpain
### Alarm
<img alt="original" src="/Example_Images_WakeUpLamp/Alarm_WakeUpLamp.PNG" height="500px" />

Set alarm to wake up
### Garlic Mode
<img alt="original" src="/Example_Images_WakeUpLamp/GarlicMode_WakeUpLamp.PNG" height="500px" />

Fun mode with garlic and lamps dropping down from the top

## License
[MIT](https://choosealicense.com/licenses/mit/)

