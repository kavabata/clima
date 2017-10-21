import datetime
import time
from schedule import get_stage, get_light
from db import get_dry_hour, add_log, add_pin, get_config, get_water_pour, add_water, set_config
from config import pin
import RPi.GPIO as GPIO
import sys

config = get_config()
stage = get_stage()
light = 3 if get_light() else 6
water_pour = get_water_pour(light)
(s1, s2, s3, s4, cnt) = get_dry_hour()
#print("%d %d %d %d == %d" % (s1, s2, s3, s4, cnt))
dict = {1: s1, 2: s2, 3: s3, 4: s4}
print "Left hours %s WP %s" % (light, water_pour)

# start gpio opration, set and clove valves
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin['rele']['pump'], GPIO.OUT)
GPIO.output(pin['rele']['pump'], GPIO.HIGH)

for valve in range(1,5):
  GPIO.setup(pin['rele'][valve], GPIO.OUT)
  GPIO.output(pin['rele'][valve], GPIO.HIGH)

if len(sys.argv) == 2:
  valve = int(sys.argv[1])
  if valve not in {1,2,3,4}:
    exit(0)


  # start delay
  if int(config['box.water.manual.%s' % (valve)]) > 0:
    runtime = int(config['box.water.manual.%s' % (valve)]) / 6 # /5
  else:
    runtime = int(config['box.water.time.%s' % (valve)]) # /5

  print "runtime %s" % (runtime)

  # open valve
  print "OPEN VALVE %d" % (valve)
  GPIO.output(pin['rele'][valve], GPIO.LOW)
  add_pin("VAL%d" % (valve), "OPEN")

  # run pump
  print "RUN PUMP"
  GPIO.output(pin['rele'][5], GPIO.LOW)
  add_pin("Pump", "OPEN")


  for x in range(1, runtime + 1):
    print "Remind %d sec of %d sec" % (x, runtime)
    time.sleep(1)

  # close valve
  print "CLOSE VALVE %d" % (valve)
  GPIO.output(pin['rele'][valve], GPIO.HIGH)
  add_pin("VAL%d" % (valve), "CLOSE")

  # stop pump
  print "STOP PUMP"
  GPIO.output(pin['rele']['pump'], GPIO.HIGH)
  add_pin("PUMP", "OFF")

  # add log
  volume = int(runtime * float(config['can.water.1']))
  left = int(config['can.left.1']) - volume

  print "volume %s" % (volume)
  print "Left %s" % (left)
  add_water('VAL%d' % (valve), runtime, volume)
  set_config('can.left.1', left)
  exit(0)

# check if log works
if int(cnt) < 1:
  print "no dry logs"
  add_log("water", "Log error, have only %d logs" % (cnt))
  exit(0)


for valve, ramp in dict.items():
  # operate valve
  print "Operate Valve %d" % valve

  if config['box.water.status.%s' % (valve)] == '1':
    # box enabled

    if int(config['box.water.manual.%s' % (valve)]) > 0:
      # manual schedule 4 times a day
      print "Manual %s" % config['box.water.manual.%s' % (valve)]

      if 'VAL%d' % (valve) not in water_pour:
        # wasnt puered in last 6 hours

        # open valve
        print "OPEN VALVE %d" % (valve)
        GPIO.output(pin['rele'][valve], GPIO.LOW)
        add_pin("VAL%d" % (valve), "OPEN")

        # run pump
        print "RUN PUMP"
        GPIO.output(pin['rele'][5], GPIO.LOW)
        add_pin("Pump", "OPEN")

        # start delay
        runtime = int(int(config['box.water.manual.%s' % (valve)]) / 6)
        for x in range(1, runtime + 1):
          print "Remind %d sec of %d sec" % (x, runtime)
          time.sleep(1)

        # close valve
        print "CLOSE VALVE %d" % (valve)
        GPIO.output(pin['rele'][valve], GPIO.HIGH)
        add_pin("VAL%d" % (valve), "CLOSE")

        # stop pump
        print "STOP PUMP"
        GPIO.output(pin['rele']['pump'], GPIO.HIGH)
        add_pin("PUMP", "OFF")

        # add log
        volume = int(runtime * float(config['can.water.1']))

        left = int(config['can.left.1']) - volume
        print "runtime %s" % (runtime)
        print "volume %s" % (volume)
        print "Left %s" % (left)
        add_water('VAL%d' % (valve), runtime, volume)
        set_config('can.left.1', left)
    else:

      if int(ramp) < int(config['box.water.limit.%d' % (valve)]):
        # ramp limit exceed

        # open valve
        print "OPEN VALVE %d" % (valve)
        GPIO.output(pin['rele'][valve], GPIO.LOW)
        add_pin("VAL%d" % (valve), "OPEN")

        # run pump
        print "RUN PUMP"
        GPIO.output(pin['rele'][5], GPIO.LOW)
        add_pin("Pump", "OPEN")

        # start delay
        runtime = int(config['box.water.time.%s' % (valve)])
        for x in range(1, runtime + 1):
          print "Remind %d sec of %d sec" % (x, runtime)
          time.sleep(1)

        # close valve
        print "CLOSE VALVE %d" % (valve)
        GPIO.output(pin['rele'][valve], GPIO.HIGH)
        add_pin("VAL%d" % (valve), "CLOSE")

        # stop pump
        print "STOP PUMP"
        GPIO.output(pin['rele']['pump'], GPIO.HIGH)
        add_pin("PUMP", "OFF")

        # add log
        volume = int(runtime * float(config['can.water.1']))
        add_water('VAL%d' % (valve), runtime, volume)
        left = int(config['can.left.1']) - volume
        set_config('can.left.1', left)

exit(0)

if int(cnt) < 30:
  print("Log error, have only %d logs" % (cnt))
  add_log("water", "Log error, have only %d logs" % (cnt))
  exit(0)

box_flow = {}

def get_flow_time(ramp):
  return int( water_conf['max'] * (int(ramp) - water_conf['ramp']) / (100 - water_conf['ramp']) ) + 1

# start gpio opration, set and clove valves
print "Set default valve and pump state"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin['rele']['pump'], GPIO.OUT)
GPIO.output(pin['rele']['pump'], GPIO.HIGH)

for valve in range(1,5):
  GPIO.setup(pin['rele'][valve], GPIO.OUT)
  GPIO.output(pin['rele'][valve], GPIO.HIGH)


run_pump = False
max_flow_time = 1

for valve, ramp in {1: s1, 2: s2, 3: s3, 4: s4}.items():
  if ramp > water_conf['ramp'] and sits[valve]['Status'] == True:
    run_pump = True
    print "Box %d need to water, ramp: %d" % (valve, ramp)
    add_log("water", "Box %d need to water, ramp: %d" % (valve, ramp))
    box_flow[valve] = get_flow_time(ramp)
    if max_flow_time < box_flow[valve]:
      max_flow_time = box_flow[valve]

    print "Open valve %d" % (valve)
    GPIO.output(pin['rele'][valve], GPIO.LOW)
    add_pin("VAL%d" % (valve), "OPEN")

if run_pump == False:
  print "No need to water"
  add_log("water", "No need to water")
  exit(0)

print "Run pump..."
GPIO.output(pin['rele'][5], GPIO.LOW)
add_pin("Pump", "OPEN")
add_log("water", "Run pump for: %d" % (max_flow_time))

# count time
for x in range(1, max_flow_time + 1):
  for (valve, sec) in box_flow.items():
    if x == sec:
      print "Close valve %d" % valve
      GPIO.output(pin['rele'][valve], GPIO.HIGH)
      add_pin("VAL%d" % (valve), "CLOSE")
  time.sleep(1)
  print "Remind %d sec of %d sec" % (x, max_flow_time)

print "Pump off."
GPIO.output(pin['rele']['pump'], GPIO.HIGH)
add_pin("PUMP", "OFF")
exit(0)

#temperature_limits = {'grow_min': 22, 'grow_max': 27, 'bloom_min': 22, 'bloom_max': 28}
#humidity_limits = {'grow_min': 50, 'grow_max': 90, 'bloom_min': 70, 'bloom_max': 99}
