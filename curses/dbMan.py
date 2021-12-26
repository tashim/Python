
import MySQLdb  # mysql library

# SERVER_USERNAME = "vadim"
# SERVER_PASSWORD = "!1+=2018Y"
# SERVER_NAME = "192.168.1.63"
# DATABASE_NAME = "studentsTest2"
import pymysql
#
SERVER_USERNAME = "root"
SERVER_PASSWORD = "1234"
SERVER_NAME = "localhost"
DATABASE_NAME = "studentstest2"


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


