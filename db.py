import MySQLdb
import pprint

config = {
  'user': 'clima',
  'password': 'clima123!',
  'host': '127.0.0.1',
  'database': 'clima',
  'raise_on_warnings': True,
  'use_pure': False,
}

db = MySQLdb.connect(
    user='clima',
    passwd='',
    host='127.0.0.1',
    db='clima')


def add_temperature_log(temp, hum):
    cursor = db.cursor()
    query = ("INSERT INTO temperature (`temperature`, `humidity`, `created`)"
	" VALUES (%s, %s, NOW())")
    data = (round(temp,2), round(hum,2))
    cursor.execute(query, data)
    db.commit()
    cursor.close()

    print 'Add to Mysql' 


def add_dry_log(data):
    cursor = db.cursor()
    query = ("INSERT INTO dry (`sensor_1`, `sensor_2`, `sensor_3`, `sensor_4`, `created`)"
        " VALUES (%s, %s, %s, %s, NOW())")
    cursor.execute(query, data)
    db.commit()
    cursor.close()

def add_pin(action, message):
    cursor = db.cursor()
    query = ("INSERT INTO pins (`action`, `message`, `created`)"
        " VALUES (%s, %s, NOW())")
    data = (action, message)
    cursor.execute(query, data)
    db.commit()
    cursor.close()

def add_log(action, message):
    cursor = db.cursor()
    query = ("INSERT INTO logs (`action`, `message`, `created`)"
        " VALUES (%s, %s, NOW())")
    data = (action, message)
    cursor.execute(query, data)
    db.commit()
    cursor.close()

def get_dry_hour():
    cursor = db.cursor()

    query = ("SELECT "
        "round((1 - sum(sensor_1)/count(*)) * 100 ) as s1,"
        "round((1 - sum(sensor_2)/count(*)) * 100 ) as s2,"
        "round((1 - sum(sensor_3)/count(*)) * 100 ) as s3,"
        "round((1 - sum(sensor_4)/count(*)) * 100 ) as s4,"
        "count(*) as cnt FROM dry"
        " WHERE created > DATE_SUB(NOW(), INTERVAL 24 HOUR)")
    cursor.execute(query,())
    data = cursor.fetchall()
    
    db.commit()
    cursor.close()

    return (data[0][0], data[0][1], data[0][2],  data[0][3], data[0][4])


def get_log(action):
    cursor = db.cursor()
    query = ("SELECT message FROM logs "
        "WHERE `action` = '" + action + "' "
        "ORDER BY id DESC "
        "LIMIT 1")
    cursor.execute(query,())
    if cursor.rowcount > 0:
       data = cursor.fetchall()
       message = data[0][0]
    else:
       message = ""

    db.commit()
    cursor.close()
    return message

def get_pin(action):
    cursor = db.cursor()
    query = ("SELECT message FROM pins "
        "WHERE `action` = '" + action + "' "
        "AND created > DATE_SUB(NOW(), INTERVAL 1 HOUR) "
        "ORDER BY id DESC "
        "LIMIT 1")
    cursor.execute(query,())
    if cursor.rowcount > 0:
       data = cursor.fetchall()
       message = data[0][0]
    else:
       message = ""

    db.commit()
    cursor.close()
    return message


def add_water(valve, delay, volume):
    cursor = db.cursor()
    query = ("INSERT INTO water (`valve`, `delay`, `volume`, `created`)"
             " VALUES (%s, %s, %s, NOW())")
    data = (valve, delay, volume)
    cursor.execute(query, data)
    db.commit()
    cursor.close()

def get_config():
    cursor = db.cursor()
    query = ("SELECT name, value FROM config ")
    cursor.execute(query,())
    result = {}
    if cursor.rowcount > 0:
        data = cursor.fetchall()
        for row in data:
            result[row[0]] = row[1]
    else:
        message = ""

    db.commit()
    cursor.close()
    return result

def set_config(key, value):
    cursor = db.cursor()
    query = ("UPDATE config SET value = %s WHERE name = %s LIMIT 1")
    cursor.execute(query,(value, key))
    db.commit()
    cursor.close()

def get_water_pour():
    cursor = db.cursor()
    query = ("SELECT valve, sum(delay) as delay FROM water "
    "WHERE created > date_sub(now(), interval 6 hour) "
    "GROUP BY valve "
    "ORDER BY valve")
    cursor.execute(query,())
    result = {}
    if cursor.rowcount > 0:
        data = cursor.fetchall()
        for row in data:
            result[row[0]] = row[1]
    else:
        message = ""

    db.commit()
    cursor.close()
    return result
