
import pymysql
import MySQLdb  # mysql library
from datetime import datetime

SERVER_USERNAME = "vadim"
SERVER_PASSWORD = "!1+=2018Y"
SERVER_NAME = "192.168.1.63"
DATABASE_NAME = "smartcv"
# SERVER_USERNAME = "root"
# SERVER_PASSWORD = "1234"
# SERVER_NAME = "localhost"
# DATABASE_NAME = "SmartCV"

global cursor
global n1
global n2
n1 = n2 = 0

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

def input(dic):
    global db
    global cursor

    if (dic["telefon"] == '' or dic["telefon"] == ' ') and (dic["email"] == '' or dic["email"] == ' ' ) :
        print('Not get telefon number and mail')
        return 'error Not get telefon number and mail'
    srez = ''
# find by telefon
    dic['name'] = dic['name'].replace('  ',' ').strip()
    dic['fname'] = dic['fname'].replace('  ',' ').strip()
    if len(dic['name']) > 24: dic['name'] = dic['name'][:24]
    if len(dic['fname']) > 24: dic['fname'] = dic['fname'][:24]
    id = None
    activ = 0
    test = "select entryID,Phone1,Email,Activities from Individual where Phone1 =  %s OR Email =  %s;"
    if cursor.execute(test,(dic['telefon'],dic['email'])) == 0:
        id = None
    else:

        rez = cursor.fetchall()
        # print('found ',len(rez),'lines')
        for cur in rez:
            # print(cur)
            if cur[1].replace('-','').strip() == dic['telefon']:
                id = cur[0]
                activ = cur[3]
                if not dic['email'] or len(dic['email']) < 6  :
                    dic['email'] = cur[2]
                # break
        if not id:
            for cur in rez:

                if cur[2] == dic['email']:
                    id = cur[0]
                    activ=cur[3]
                    srez += "\nchange telefon "+str(cur)
                    activ = 1000
                    break

    if id:
        if activ == 201: return  srez + ' \n OK ' +dic['telefon']
        # TODO if exist Update set Activitis 201
        srez =srez + '\n exist in DB :'+dic['telefon']
        cursor.execute("Update Individual set "
                       "Phone1 = %s, "
                       "Email = %s, "
                       "FirstName = %s," 
                       "LastName = %s," 
                       "Activities = %s "
                       "where entryID = %s;",
                           (
                        dic['telefon'],
                        dic['email'],
                        dic['fname'],
                        dic['name'],
                        201,
                        id
                       )  )
        srez +='\n Update '+dic['telefon']
        db.commit()
        # print(' not found')
    else:
        # TODO else input to DB
        if not 'city' in dic: dic['city'] =None
        if not 'ContactType' in dic: contact =100
        else:
            if (cursor.execute("select codeID from ContactTypes where type=%s",dic['ContactType']) ==0):
                cursor.execute("select codeID from ContactTypes order by codeID desc limit 1;")
                contact = cursor.fetchone()[0]+1
                cursor.execute('INSERT INTO contacttypes (codeID, type) VALUES (%s, %s);',(contact,dic['ContactType']))
                db.commit()
            else:
                contact = cursor.fetchone()[0]
        savequery = "INSERT INTO Individual(" \
                    "EntryDate," \
                    "FirstName," \
                    "LastName," \
                    "Phone1," \
                    "Email," \
                    "ContactType," \
                    "City," \
                    "Activities" \
                    ")" \
            "VALUES(%s, %s,  %s, %s, %s , %s, %s ,%s) ;"
        cursor.execute(savequery, (
            dic["date"],
            dic["name"],
            dic["fname"],
            dic["telefon"],
            dic["email"],
            contact,
            dic['city'],
            201
        ) )
        srez +='\ninsert ' + dic['telefon']
        db.commit()
        ### get id
        if cursor.execute(test, (dic['telefon'], dic['email'])) == 0:
            id = None
            srez +='\n ::: error insert'
        else:
            id = cursor.fetchone()[0]
        if id:
            cursor.execute("insert into Comments (parID,contents) values (%s,%s)", (id, ' copy from BMBY '))
            db.commit()

    return srez
