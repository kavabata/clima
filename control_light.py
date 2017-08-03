from config import pin, temperature, humidity, light_conf
from db import add_log, add_pin
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin['rele']['led'], GPIO.OUT)
GPIO.setup(pin['rele']['dlr'], GPIO.OUT)
GPIO.setup(pin['rele']['hum'], GPIO.OUT)





device_args = { 'dlr': pin['rele']['dlr'],
                'led': pin['rele']['led'],
                'hum': pin['rele']['hum'] }
control_args = { 'on': GPIO.LOW, 'off': GPIO.HIGH }

if len(sys.argv) == 3 and sys.argv[1] in device_args and sys.argv[2] in control_args:
    dpin = device_args[sys.argv[1]]
    control = control_args[sys.argv[2]]
else:
    print('usage: control_light.py [dlr|led|hum] [on|off]')
    sys.exit(1)


GPIO.output(dpin, control)

