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

# pin['rele']['led'] = 12 #
# pin['rele'][6] = 12 # 32 # d led light

# pin['rele']['dlr'] = 16
# pin['rele'][7] = 16 # 36 # d dlr light

pin['rele']['hum'] = 20
pin['rele'][8] = 20 # 38 # d humidity   #high=off

pin['rele']['led'] = 5 # 29
pin['rele']['dlr'] = 20 # 31
pin['rele']['fan'] = 20 # 31

# temperature sensor
pin['dht'] = 21 # 40 #bcm