from config import pin, temperature, humidity, light_conf
from db import add_log
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin['rele']['led'], GPIO.OUT)
GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
GPIO.setup(pin['rele']['hum'], GPIO.OUT)

GPIO.output(pin['rele']['led'], GPIO.HIGH)
GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
GPIO.output(pin['rele']['hum'], GPIO.HIGH)

add_log("LED", "HIGH")
add_log("DLR", "HIGH")
add_log("HUM", "HIGH")
print "DLR, LED, HUM - OFF"
