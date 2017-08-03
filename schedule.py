from config import light_conf, bloom_date
import datetime
import time
import datetime

def get_stage():
    today = int(datetime.datetime.now().strftime("%Y%m%d"))
    if today > bloom_date:
      return 'bloom'
    else:
      return 'vega'

def get_light_sch():
    stage = get_stage()
    hour = int(datetime.datetime.now().strftime("%H"))
    start = int(light_conf[stage]['start'])
    end = int(light_conf[stage]['end'])
    return (hour, start, end)

def get_light():
    shoot = False
    (hour, start, end) = get_light_sch()

    if start < end:
        print "Light: day mode"
        if hour >= start and hour < end:
            shoot = True
    else:
        print "Light: night mode"
        if hour >= start or hour < end:
            shoot = True
    
    if shoot:
       print "Light ON"
    else:
       print "Light OFF"

    return shoot

print get_stage()
