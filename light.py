import sys
from config import pin, light_conf
from schedule import get_stage, get_light
from db import add_log
import RPi.GPIO as GPIO

stage = get_stage()
light_mode = get_light()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin['rele']['led'], GPIO.OUT)
GPIO.setup(pin['rele']['dlr'], GPIO.OUT)


if light_mode:
  add_log("DLR", "LOW")
  add_log("LED", "LOW")
  GPIO.output(pin['rele']['dlr'], GPIO.LOW)
  GPIO.output(pin['rele']['led'], GPIO.LOW)
else:
  add_log("DLR", "HIGH")
  add_log("LED", "HIGH")
  GPIO.output(pin['rele']['dlr'], GPIO.HIGH)
  GPIO.output(pin['rele']['led'], GPIO.HIGH)


