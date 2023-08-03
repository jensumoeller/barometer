import time
import board
import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()

print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
print('QFE = {0:0.2f} Pa'.format(sensor.read_pressure()/100))
print('Alt = {0:0.2f} m'.format(sensor.read_altitude()))
print('QNH = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()/100))

