import sys
from config import pin
from schedule import get_stage, get_light
from db import add_pin, get_config
import RPi.GPIO as GPIO

stage = get_stage()
light_mode = get_light()
config = get_config()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin['rele']['led'], GPIO.OUT)
GPIO.setup(pin['rele']['dlr'], GPIO.OUT)


if light_mode and config['general.silent'] == '0':
  add_pin("DLR", "ON")
  add_pin("LED", "ON")
  GPIO.output(pin['rele']['dlr'], GPIO.LOW)
  GPIO.output(pin['rele']['led'], GPIO.LOW)
else:
  add_pin("DLR", "OFF")
  add_pin("LED", "OFF")
  GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
  GPIO.output(pin['rele']['led'], GPIO.HIGH)


