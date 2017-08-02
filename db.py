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
    passwd='clima123!',
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

def add_log(action, message):
    cursor = db.cursor()
    query = ("INSERT INTO logs (`action`, `message`, `created`)"
        " VALUES (%s, %s, NOW())")
    data = (action, message)
    cursor.execute(query, data)
    db.commit()
    cursor.close()

def get_dry_hour(light):
    cursor = db.cursor()
    if light:
      interval = 2
    else:
      interval = 4
    query = ("SELECT "
        "sum(sensor_1)*100/count(*) as s1,"
        "sum(sensor_2)*100/count(*) as s2,"
        "sum(sensor_3)*100/count(*) as s3,"
        "sum(sensor_4)*100/count(*) as s4,"
        "count(*) as cnt FROM dry"
        " WHERE created > DATE_SUB(NOW(), INTERVAL 1 HOUR)")
    cursor.execute(query,())
    data = cursor.fetchall()
    
    db.commit()
    cursor.close()
    return data[0]
    #return (69, 79, 89, 99, 33)


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

