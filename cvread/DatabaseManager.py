"""Function to insert extracted info to a database"""

# Imports
import pymysql
import MySQLdb  # mysql library
from datetime import datetime
import sys
from Scanners import addUCounter
from Scanners import addACounter

# DB function has several different ready to work sql queries to match the data needed to fill in the Local DB
# Uses the given host to connect to the DB and Save\Update the info in the DB
def saveData(person_data, text, location, service):
    testquery = "select (1) from Individual where Phone1 = '" + person_data[2] + "' limit 1;"
    testquery2 = "select (1) from Individual where Phone1 = '" + person_data[2] + "' and EntryDate < DATE_SUB(NOW(),INTERVAL 1 YEAR);"

    savequery = "INSERT INTO Individual(FirstName,DateOfBirth,Phone1,Email,ContactType,Activities, CV, file_path)" \
                "VALUES(%s, %s, %s, %s, " + service + ", 200, %s, %s);"
    idquery = "Select entryID from Individual where Phone1='" + person_data[2] + "';"

    savequery2 = "INSERT INTO Domains_list (entryID, Domain)" \
                 "VALUES(%s, 300);"

    savequery7 = "INSERT INTO Skills (parID) values (%s)"

    savequery3 = "INSERT INTO testGrade (parID) values (%s)"

    savequery4 = "INSERT INTO Experience (parID) values (%s)"

    savequery5 = "INSERT INTO Education (parID) values (%s)"

    savequery6 = "INSERT INTO MeetingsDate (parID) values (%s)"

    updatequery = """UPDATE Individual
                  SET FirstName=%s, DateOfBirth=%s, Phone1=%s, Email=%s, CV=%s, file_path=%s
                  WHERE Phone1=%s"""

    updatequery2 = """UPDATE Individual
                      SET FirstName=%s, DateOfBirth=%s, Phone1=%s, Email=%s, CV=%s, Activities=%s, NewEntryDate=%s, file_path=%s
                      WHERE Phone1=%s"""
    activities = 200
    date = str(datetime.now())

    save_args = (person_data[0], person_data[1], person_data[2], person_data[3], text, location)
    update_args = (person_data[0], person_data[1], person_data[2], person_data[3], text, location, person_data[2])
    update_args2 = (person_data[0], person_data[1], person_data[2], person_data[3], text, activities, date, location, person_data[2])
    # print info_args

    cursor = None
    conn = None
    result = 0
    # host2 = sys.argv[1]
    # user = sys.argv[2]
    # password = sys.argv[3]
    # database = sys.argv[4]

    host2 = '192.168.1.63'
    user = 'vadim'
    password = '!1+=2018Y'
    database = 'smartcv'

    try:
        conn = pymysql.connect(host2, user, password, database, charset='utf8')
        print(person_data)
        # print(text)
        print(location)
        cursor = conn.cursor()
        result = 0

        if cursor.execute(testquery) == 0:
            print("new ")
            cursor.execute(savequery, save_args)
            cursor.execute(idquery)
            parid = cursor.fetchone()
            print("parID = ",parid)
            cursor.execute(savequery2, parid)
            cursor.execute(savequery3, parid)
            cursor.execute(savequery4, parid)
            cursor.execute(savequery5, parid)
            cursor.execute(savequery6, parid)

            cursor.execute(savequery7, parid)
            conn.commit()
            addACounter(1)
            result = 1
            print ("Entry saved to Database!")
            # cursor = None
            # cursor = conn.cursor()

        elif cursor.execute(testquery) == 1:
            print("exist")
            if cursor.execute(testquery2) == 1:
                cursor.execute(updatequery2, update_args2)
                conn.commit()
                addUCounter(1)
                result = 1
                print ("Entry updated in Database!")
            else:
                cursor.execute(updatequery, update_args)
                conn.commit()
                addUCounter(1)
                result = 1
                print ("Entry updated in Database!")


    except MySQLdb.Error as e:
        print("error conn")
        conn.rollback()
        print (e)

    finally:
        # cursor.close()
        # conn.close()
        return result
