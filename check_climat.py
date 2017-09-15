import sys
import Adafruit_DHT as dht
from config import pin
from schedule import get_stage, get_light
from db import add_temperature_log, add_log, get_log, get_pin, add_pin, get_config
import RPi.GPIO as GPIO

config = get_config()
sensor = dht.AM2302

hum, temp = dht.read_retry(sensor, pin['dht'])
stage = get_stage()
light_mode = get_light()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

if hum is not None and temp is not None:
    add_temperature_log(temp, hum)
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temp, hum))

    if temp > config['climat.temperature.max']:
        if get_pin("DLR") != "OFF":
            add_log("clima", "EXTREME temperature")

            GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
            GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
            add_pin("DLR", "OFF")

    elif temp < config['climat.temperature.min']:

        if get_pin("DLR") != "ON":
            add_log("clima", "cold temperature")
            GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
            GPIO.output(pin['rele']['dlr'], GPIO.LOW)
            add_pin("DLR", "ON")
    else:
        print('Temp is OK')

else:
    add_log("clima", "Failed to get reading. Try again!")
    print('Failed to get reading. Try again!')
    sys.exit(1)

