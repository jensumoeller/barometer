import time
import numpy as np
import board
import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085

# Setze den GPIO-Modus auf BCM für die Ansteuerung der LED
GPIO.setmode(GPIO.BCM)

# Definiere die GPIO-Pins für die LEDs
led_grn = 4
led_red = 17

# Initialisiere die GPIO-Pins als Ausgänge
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_grn, GPIO.OUT)

# Initialisiere den Adafruit BMP185 Luftdrucksensor
sensor = BMP085.BMP085()

# Ermitteln des durchschnittlichen QFE aus 10 Messungen
def qfe_mittel():
    luftdruck = []        #Array initialisieren
    for i in range(10):
        luftdruck.append(sensor.read_pressure())
        time.sleep(10)    #10 Sekunden warten bis zur nächsten Messung
        
    return np.mean(luftdruck)/100

# Auslesen der Temperatur
def temperatur():
    temperatur = sensor.read_temperature()

    return temperatur

# Schalten der LED auf rot oder grün
def anzeige(farbe):
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

    # Initialisieren der Variable für aktuellen Luftdruck
    qfe_neu = 1013.25     # Initialer Luftdruck in hPa für Vergleich
    delta = 0.1           # minimaler Differenzdruck für Trend
    intervall = 30        # Intervalldauer der Messungen in Minuten
    anzeige('beide')      # beide LED initial an

    while True:
        qfe_alt = qfe_neu
        qfe_neu = qfe_mittel()

        if qfe_neu - qfe_alt > delta:   # Luftdruck steigt
            anzeige('gruen')
        elif qfe_alt - qfe_neu > delta: # Luftdruck fällt
            anzeige('rot')
        else:                           # Luftdruck konstant
            anzeige('beide')

        print('QFE = {0:0.1f} hPa'.format(qfe_mittel()))
        print('Temp = {0:0.1f} *C'.format(temperatur()))
        # print('Alt = {0:0.2f} m'.format(sensor.read_altitude()))
        # print('QNH = {0:0.2f} hPa'.format(sensor.read_sealevel_pressure()/100))

        time.sleep(intervall * 60)
        

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()

