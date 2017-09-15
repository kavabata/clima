from config import pin, temperature, humidity, light_conf
from db import add_log, add_pin
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin['rele']['led'], GPIO.OUT)
GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
GPIO.setup(pin['rele']['hum'], GPIO.OUT)
GPIO.setup(pin['rele']['fan'], GPIO.OUT)

GPIO.output(pin['rele']['led'], GPIO.LOW)
GPIO.output(pin['rele']['dlr'], GPIO.LOW)
GPIO.output(pin['rele']['hum'], GPIO.LOW)
GPIO.output(pin['rele']['fan'], GPIO.LOW)

add_pin("LED", "ON")
add_pin("DLR", "ON")
add_pin("HUM", "ON")
add_pin("FAN", "ON")
print "DLR, LED, HUM, FAN - ON"
