import time
import numpy as np
import board
import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image

# Setze den GPIO-Modus auf BCM für die Ansteuerung der LED
GPIO.setmode(GPIO.BCM)

# Definiere die GPIO-Pins für die LEDs
led_grn = 20
led_red = 21

# Initialisiere die GPIO-Pins als Ausgänge
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_grn, GPIO.OUT)

# Initialisiere den Adafruit BMP185 Luftdrucksensor
sensor = BMP085.BMP085()

# Initialisieren des OLED Displays
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, height=32, width=128, rotate=0)


# Ermitteln des durchschnittlichen QFE aus 10 Messungen
def qfe_mittel():
    luftdruck = []        #Array initialisieren
    for i in range(10):
        luftdruck.append(sensor.read_pressure())
        time.sleep(1)    #1 Sekunde warten bis zur nächsten Messung
        
    return np.mean(luftdruck)/100

# Auslesen der Temperatur
def temperatur():
    temperatur = sensor.read_temperature()

    return temperatur

# Schalten der LED auf rot oder grün
def led_anzeige(farbe):
    if farbe == 'rot':
        GPIO.output(led_red, GPIO.HIGH)
        GPIO.output(led_grn, GPIO.LOW)
    elif farbe == 'gruen':
        GPIO.output(led_red, GPIO.LOW)
        GPIO.output(led_grn, GPIO.HIGH)
    elif farbe == 'beide':
        GPIO.output(led_red, GPIO.HIGH)
        GPIO.output(led_grn, GPIO.HIGH)
    else:
        GPIO.output(led_red, GPIO.LOW)
        GPIO.output(led_grn, GPIO.LOW)


# ====== HAUPTPROGRAMM =======
def main():

    # Schriftart für das OLED-Display setzen
    oled_font = ImageFont.truetype('FreeSans.ttf', 14)

    # Iitialisieren der Variable für aktuellen Luftdruck
    qfe_neu = 1013.25     # Initialer Luftdruck in hPa für Vergleich
    delta = 0.3           # minimaler Differenzdruck für Trend
    intervall = 30        # Intervalldauer der Messungen in Minuten
    led_anzeige('beide')  # beide LED initial an

    while True:
        led_anzeige('')                 # LED aus bei Ermittlung
        with canvas(device) as draw:
            # draw.rectangle(device.bounding_box, outline = "white", fill = "black")
            draw.text((2, 2), "Messung ...", font = oled_font, fill = "white")

        qfe_alt = qfe_neu
        qfe_neu = qfe_mittel()

        if qfe_neu - qfe_alt > delta:   # Luftdruck steigt
            led_anzeige('gruen')
        elif qfe_alt - qfe_neu > delta: # Luftdruck fällt
            led_anzeige('rot')
        else:                           # Luftdruck konstant
            led_anzeige('beide')
        
        # print('QFE = {0:0.1f} hPa'.format(qfe_mittel()))
        # print('Temp = {0:0.1f} *C'.format(temperatur()))
        # print('Alt = {0:0.2f} m'.format(sensor.read_altitude()))
        # print('QNH = {0:0.2f} hPa'.format(sensor.read_sealevel_pressure()/100))

        # Ermittlung und Format der UTC-Zeit und des Luftdrucks
        aktuelle_zeit_utc = time.strftime('%H:%M', time.gmtime(time.time()))
        qfe_formatiert = "{:.1f}".format(qfe_neu)
        qfe_delta_formatiert = "{:.1f}".format(qfe_neu - qfe_alt)

        # Ausgabe über OLED Display
        oled_ausgabe = 'QFE ' + qfe_formatiert + '  (' + qfe_delta_formatiert + ')'
        with canvas(device) as draw:
            draw.text((0, 0), oled_ausgabe, font = oled_font, fill = "white")
            draw.text((0,18), aktuelle_zeit_utc +'Z', font = oled_font, fill = "white")

        time.sleep(intervall * 60)
        

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()

