
import MySQLdb  # mysql library

import pymysql

DATABASE_NAME = "studentsTest2"
# DATABASE_NAME = "smartcv"

db_place = 3
if db_place==0:
    SERVER_USERNAME = "root"
    SERVER_PASSWORD = "1234"
    SERVER_NAME = "localhost"
elif  db_place==1:
    SERVER_USERNAME = "vadim"
    SERVER_PASSWORD = "!1+=2018Y"
    SERVER_NAME = "192.168.1.63"
else:
    SERVER_USERNAME = "appdev"
    SERVER_PASSWORD = "Tengrinews1965"
    SERVER_NAME = "45.83.43.173"

print(SERVER_NAME)

def con_close(db):
    db.cursor.close()
    db.close()

def connnect():
    try:
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
        return db
    except MySQLdb.Error as e:
        print("error conn")
        db.rollback()
        print (e)
        return  0

def get_curs_c(db):
    db.cursor().execute('SELECT * FROM coursecycle;')
    cursess = db.cursor().fetchall()
    return cursess


