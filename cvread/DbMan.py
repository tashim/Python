
import pymysql
import MySQLdb  # mysql library
from datetime import datetime
from Scan import addACounter, addUCounter

SERVER_USERNAME = "vadim"
SERVER_PASSWORD = "!1+=2018Y"
SERVER_NAME = "192.168.1.63"
DATABASE_NAME = "smartcv"

# SERVER_USERNAME = "root"
# SERVER_PASSWORD = "1234"
# SERVER_NAME = "localhost"
# DATABASE_NAME = "SmartCV"

global cursor
testquery = "select entryID from Individual where Phone1 =  %s limit 1;"
# savequery = "INSERT INTO Individual(FirstName,LastName,Phone1,Email)" \
#             "VALUES('vasa', '%s','059888', '%s');"
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

def setDB(dic):
    # print('setDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    if dic["telefon"] == '' or dic["telefon"] == ' ' :
        print('Not get telefon number')
        return
    global db
    global cursor
### print for debug dict
    # for l in dic:    print(l, '\t:', dic[l])
### check telefon if is true
    if len(dic["name"])>21:dic["name"]=dic["name"][0:21]
    if len(dic['telefon']) < 8:    return 0
    dic['telefon'] = dic['telefon'].strip()
    if not dic['telefon'].isdigit():   return 0
### if domain exist
    dic['domain'] = dic['domain'].replace('\n','')
    dic['domain'] = dic['domain'].replace('\r','')
    dic['domain'] = dic['domain'].strip()

    dom = None
    if dic['domain'] != '' and dic['domain'] != ' ':
        dom = cursor.execute("select codeID from Domains where domain = %s", dic['domain'])
        if dom:
            dom = cursor.fetchone()[0]
            # print('dom = ', int(dom[0]))
        else:
            cursor.execute("select codeID from Domains order by codeID desc limit 1;")
            dom = cursor.fetchone()[0] + 1
            cursor.execute('insert into Domains (codeID,domain) values ("%s",%s);', (dom, dic['domain']))
            db.commit()



    dic['comment'] = "lid from"+dic['service']+": " + dic['domain']
        ### if telefon exist in DB
    id = None
    if cursor.execute(testquery ,dic["telefon"]) == 0:
        # print('newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        try:
### insert new entry
            savequery = "INSERT INTO Individual(FirstName,LastName,Phone1,Email,ContactType,personID,CV,0us_1him,Activities)" \
                        "VALUES(%s, %s, %s, %s ,%s , %s, %s ,1,200);"
            cursor.execute(savequery,(dic["name"],dic["fname"],dic["telefon"],dic["email"],dic['ContactType'],dic['TZ'],dic['CV']))
            db.commit()
            addACounter(1)
###  Get his ID
            id = None
            if cursor.execute("Select entryID from Individual where Phone1=%s;", (dic["telefon"],)):
                id= cursor.fetchone()[0]
### set Doomain in DomainList
                if dom and id: cursor.execute("insert into Domains_list (entryID,Domain) values ( %s , %s )",(id,dom))
###
### set comments:
###
            if id: cursor.execute("insert into Comments (parID,contents) values (%s,%s)", (id, dic['comment']))
            db.commit()
        except MySQLdb as e:
            print(e)
            dic['comment']
        except:
            print('eror')
        print("new",dic["telefon"])
    else:
        # print('oldddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        id = cursor.fetchone()[0]
        if id:cursor.execute("select entryID from Domains_list where entryID=%s and Domain=%s limit 1;",(id,dom))
        if not cursor.fetchone():
            cursor.execute("insert into Domains_list (entryID,Domain) values ( %s , %s ); ",(id,dom))

        cursor.execute("select 1 from Comments where parID=%s and contents=%s limit 1;",(id,dic['comment']))
        if not cursor.fetchone():
            cursor.execute("insert into Comments (parID,contents) values (%s,%s);", (id, dic['comment']))

        cursor.execute('update Individual set FirstName = %s,LastName = %s,Email = %s,City = %s,personID = %s,'
                   'NewEntryDate=NOW(),'
                   'ContactType=%s, CV=%s  where entryID =  %s;',
                   (
                       dic['fname'],
                       dic['name'],
                       dic['email'],
                       dic['city'],
                       dic['TZ'],
                       dic['ContactType'],
                       dic['CV'],
                       id
                   ))
        db.commit()
        addUCounter(1)
    return 1

# connnect()