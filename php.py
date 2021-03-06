import datetime
import time
from schedule import get_stage
from db import get_dry_hour, add_log, add_pin
from config import water_conf, pin, light_conf, sits
import RPi.GPIO as GPIO

stage = get_stage()

hour = int(datetime.datetime.now().strftime("%H"))
start = int(light_conf[stage]['start'])
end = int(light_conf[stage]['end'])

light_on = False
#(s1, s2, s3, s4, cnt) = get_dry_hour(light_on)
(s1, s2, s3, s4, cnt) = (88,30,30,30,50)

if int(cnt) < 30:
    print("Log error, have only %d logs" % (cnt))
    add_log("water", "Log error, have only %d logs" % (cnt))
    exit(0)

box_flow = {}

def get_flow_time(ramp):
    return int( water_conf['max'] * (int(ramp) - water_conf['ramp']) / (100 - water_conf['ramp']) ) + 1

# start gpio opration, set and clove valves
print "Set default valve and pump state"
print "IOOO"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin['rele']['pump'], GPIO.OUT)
GPIO.output(pin['rele']['pump'], GPIO.HIGH)
print "IOOO"
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

if run_pump == False:
    print "No need to water"
    exit(0)

print "Run pump..."
add_pin("Pump", "OPEN")
add_log("water", "Run pump for: %d" % (max_flow_time))

# count time
for x in range(1, max_flow_time + 1):
    for (valve, sec) in box_flow.items():
        if x == sec:
            print "Close valve %d" % valve
    time.sleep(1)
    print "Remind %d sec of %d sec" % (x, max_flow_time)

print "Pump off."
add_pin("PUMP", "OFF")
exit(0)