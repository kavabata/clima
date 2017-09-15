import db
# from config import light_conf, bloom_date
import datetime

config = db.get_config()


def get_stage():
    return 'bloom'

def get_light_sch():
    hour = int(datetime.datetime.now().strftime("%H%M"))
    start = int(config['climat.light.on'])
    end = int(config['climat.light.off'])
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
