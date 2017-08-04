
# Cam config
cam_path = "/home/pi/html/cam/"

bloom_date = 20170815

# Temperature
temperature = {'vega': {}, 'bloom': {}}
temperature['vega']['min'] = 25
temperature['vega']['max'] = 26
temperature['vega']['extreme'] = 32
temperature['bloom']['min'] = 26
temperature['bloom']['max'] = 27
temperature['bloom']['extreme'] = 35

humidity = {'vega': {}, 'bloom': {}}
humidity['vega']['min'] = 70
humidity['vega']['max'] = 80
humidity['bloom']['min'] = 50
humidity['bloom']['max'] = 60


# pin connection
pin = {'dry': {}, 'rele': {}}

# dry sensors
pin['dry'][1] = 14  # d orange
pin['dry'][2] = 15 # up green
pin['dry'][3] = 18 # d blue
pin['dry'][4] = 23 # d black

# valve operate
pin['rele'][1] = 24 # 18 # d  valve orange #low=off
pin['rele'][2] = 25 # 22 # d valve green
pin['rele'][3] = 8  # 24 # up valve blue
pin['rele'][4] = 7  # 26 # up valve black

pin['rele']['pump'] = 1 #high=off
pin['rele'][5] = 1  # 28 # up pump

pin['rele']['led'] = 12 #
pin['rele'][6] = 12 # 32 # d led light

pin['rele']['dlr'] = 16
pin['rele'][7] = 16 # 36 # d dlr light

pin['rele']['hum'] = 20
pin['rele'][8] = 20 # 38 # d humidity   #high=off

# temperature sensor
pin['dht'] = 21 # 40 #bcm


# Light configuration

light_conf = {'vega': {}, 'bloom': {}, 'stress': {}, 'test': {}}

light_conf['vega']['start'] = 20
light_conf['vega']['end'] = 14

light_conf['bloom']['start'] = 22
light_conf['bloom']['end'] = 10

light_conf['stress']['start'] = 23
light_conf['stress']['end'] = 2

light_conf['test']['test'] = 02

light_conf['led'] = False

# Water conf

water_conf = {}

water_conf['ramp'] = 50 # over 60% of dry mean start water
water_conf['max'] = 30 # seconds of max flow
