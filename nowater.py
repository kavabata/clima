import sys
from config import water_conf, pin, light_conf
import RPi.GPIO as GPIO
from db import add_log, add_pin

# start gpio opration, set and clove valves
print "Set default valve and pump state"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin['rele'][5], GPIO.OUT)
GPIO.output(pin['rele'][5], GPIO.HIGH)
add_log("PUMP", "OFF")

for valve in range(1,5):
  GPIO.setup(pin['rele'][valve], GPIO.OUT)
  GPIO.output(pin['rele'][valve], GPIO.LOW)
  add_pin("VAL%d" % (valve), "CLOSE")


