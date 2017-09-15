from config import pin
from db import add_pin
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin['rele']['led'], GPIO.OUT)
GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
GPIO.setup(pin['rele']['hum'], GPIO.OUT)
GPIO.setup(pin['rele']['fan'], GPIO.OUT)

GPIO.output(pin['rele']['led'], GPIO.HIGH)
GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
GPIO.output(pin['rele']['hum'], GPIO.HIGH)
GPIO.output(pin['rele']['fan'], GPIO.HIGH)

add_pin("LED", "OFF")
add_pin("DLR", "OFF")
add_pin("HUM", "OFF")
add_pin("FAN", "OFF")

print "DLR, LED, HUM, FAN - OFF"
