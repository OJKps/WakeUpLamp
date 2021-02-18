import smbus2
import bme280

"""
https://pypi.org/project/RPi.bme280/
No need to install i2c tools already installed
Enable i2c for settings, rpi configuration, pi user is already in the i2c group
PIN layout:
    PIN 3 is SDA
    PIN 5 is SCL
    PIN 14 GND
    PIN 1 is VCC
"""

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)


def get_bme_reads():       
    # the sample method will take a single reading and return a
    # compensated_reading object
    try:
        return bme280.sample(bus, address, calibration_params)
    except:
        return "ERROR BME SENSOR"

    # the compensated_reading class has the following attributes
    #print(data.id)
    #print(data.timestamp)
    #print(data.temperature)
    #print(data.pressure)
    #print(data.humidity)

    # there is a handy string representation too
    
