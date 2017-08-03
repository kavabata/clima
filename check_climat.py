import sys
import Adafruit_DHT as dht
from config import pin, temperature, humidity, light_conf
from schedule import get_stage, get_light
from db import add_temperature_log, add_log, get_log, get_pin, add_pin
import RPi.GPIO as GPIO

sensor = dht.AM2302

hum, temp = dht.read_retry(sensor, pin['dht'])
stage = get_stage()
light_mode = get_light()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

if hum is not None and temp is not None:
    add_temperature_log(temp, hum)
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temp, hum))

    if temp > temperature[stage]['max'] and temp < temperature[stage]['extreme']:
        add_log("clima", "high temperature")
        if light_conf['led']:
            # Off DLR only when LED available
            if get_pin("DLR") != "HIGH":
                GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
                GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
                add_pin("DLR", "OFF")

    elif temp > temperature[stage]['extreme']:
        # Off all 220
        add_log("clima", "EXTREME temperature")

        GPIO.setup(pin['rele']['led'], GPIO.OUT)
        GPIO.output(pin['rele']['led'], GPIO.HIGH)
        add_pin("LED", "OFF")

        GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
        GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
        add_pin("DLR", "OFF")

        GPIO.setup(pin['rele']['hum'], GPIO.OUT)
        GPIO.output(pin['rele']['hum'], GPIO.HIGH)
        add_pin("HUM", "OFF")

        hum = 100

    elif temp < temperature[stage]['min']:
        add_log("clima", "cold temperature")
        if light_mode:
            # Enable DLR as additional
            if get_pin("DLR") != "HIGH":
                GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
                GPIO.output(pin['rele']['dlr'], GPIO.LOW)
                add_pin("DLR", "ON")

    if hum > humidity[stage]['max'] or hum >= 100:
        # Humidiator OFF
        if get_pin("HUM") != "LOW":
            GPIO.setup(pin['rele']['hum'], GPIO.OUT)
            GPIO.output(pin['rele']['hum'], GPIO.HIGH)
            add_pin("HUM", "OFF")

    elif hum < humidity[stage]['min']:
        # Humidiator ON
        if get_pin("HUM") != "HIGH":
            GPIO.setup(pin['rele']['hum'], GPIO.OUT)
            GPIO.output(pin['rele']['hum'], GPIO.LOW)
            add_pin("HUM", "ON")

else:
    add_log("clima", "Failed to get reading. Try again!")
    print('Failed to get reading. Try again!')
    sys.exit(1)

