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

def get_sol():
    date_format = '%Y-%m-%d'
    # date_format = "%m/%d/%Y"
    print "Start Date %s" % (config['general.start'])
    a = datetime.datetime.strptime(config['general.start'], date_format)
    b = datetime.datetime.now()
    delta = b - a

    d = get_sol_delta()
    print "Days %s + Delta %s" % (delta.days, d)
    return delta.days + d

def get_sol_delta():
    sol = 0
    (hour, start, end) = get_light_sch()

    if start < end:
        print "Light: day mode"
        if hour >= start and hour < end:
            sol = 0
    else:
        print "Light: night mode"
        if hour > end:
            sol = 1
        if hour < end:
            sol = 0

    print "Sol %d" % (sol)
    return sol

print get_stage()
