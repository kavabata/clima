#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
from config import pin
from db import add_dry_log

GPIO.setmode(GPIO.BCM)

for p, v in pin['dry'].items():
    GPIO.setup(v, GPIO.IN)

data = []
for p, v in pin['dry'].items():
    data.insert(p, GPIO.input(v))

add_dry_log(data)

