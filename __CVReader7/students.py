
import pymysql
import MySQLdb  # mysql library
from datetime import datetime
#
SERVER_USERNAME = "vadim"
SERVER_PASSWORD = "!1+=2018Y"
SERVER_NAME = "192.168.1.63"
# DATABASE_NAME = "smartcv"
# SERVER_USERNAME = "root"
# SERVER_PASSWORD = "1234"
# SERVER_NAME = "localhost"
DATABASE_NAME = "studentsTest2"
# host2 = '192.168.1.63'
# user = 'vadim'
# password = '!1+=2018Y'
# database = 'smartcv'

global cursor
testquery = "select entryID from Individual where Phone1 =  %s limit 1;"
# savequery = "INSERT INTO Individual(FirstName,LastName,Phone1,Email)" \
#             "VALUES('vasa', '%s','059888', '%s');"
savequery = "INSERT INTO Individual(FirstName,LastName,Phone1,Email,ContactType,City,0us_1him,Activities)" \
            "VALUES(%s, %s, %s, %s , 101, %s ,1,200);"
def con_close():
    cursor.close()
    db.close()

def connnect():
    try:
        global db
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
        global  cursor
        cursor = db.cursor()
        return 1
    except MySQLdb.Error as e:
        print("error conn")
        db.rollback()
        print (e)
        return  0

def main():
    global db
    global cursor
    dom = cursor.execute(
        # "SHOW FULL TABLES  ;"
        # "select * from coursecycle;"
        "SELECT studentID,courseCode,openDate FROM studentspercycle "
        "inner join coursecycle on courseCycleCode=coursecycle.code "
        "where openDate < now() order by studentID ;"
    )
    r = cursor.fetchall()
    # if not r: break
    n=0
    for i in r:
        # print(i)
        # s= "SELECT student,timesRepeated,course " \
        #    "FROM coursesperstudent  where student='310894142' and course='"+str(i[1])+"';"
        dom = cursor.execute(
            "SELECT student,timesRepeated,course FROM coursesperstudent  where student=%s and course=%s and timesRepeated=0;"
            ,(i[0],i[1])
         )
        # print(s)
        rr = cursor.fetchone()
        if rr:
            n +=1
            cursor.execute("update coursesperstudent set timesRepeated=1  where student=%s and course=%s"
                           , (i[0], i[1])
                           )
            print('>>',rr)
            # for y in rr:
    print(len(r))
    print(n)
    db.commit()


connnect()
main()