
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

def set(dic):
    # print('setDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    if dic["telefon"] == '' or dic["telefon"] == ' ' :
        print('Not get telefon number')
        return

    global db
    global cursor
### print for debug dict
    # for l in dic:    print(l, '\t:', dic[l])
### check telefon if is true
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


    if 'tostudy' in dic['From']:
        dic['comment'] = "lid ToStudy: " + dic['domain']
    if 'tostudy' in dic['From']:
        dic['comment'] = "lid YORM: " + dic['comment']
    if 'rt-ed.co.il' in dic['From']:
        dic['comment'] = "lid SEO: " + dic['comment']
        ### if telefon exist in DB
    id = None
    if cursor.execute(testquery ,dic["telefon"]) == 0:
        # print('newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        try:
### insert new entry
            cursor.execute(savequery,(dic["name"],dic["fname"],dic["telefon"],dic["email"],dic['city']))
            db.commit()
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
        except:
            print('eror')
        print("new",dic["telefon"])
    else:
        # print('oldddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        id = cursor.fetchone()[0]
        if id: cursor.execute('select FirstName,LastName,Email,City,ContactType,Activities from Individual where entryID =  %s limit 1; ',id)
        else: return
        L1=['fname','name','email','city','ContactType','Activities']

        L2 = cursor.fetchone()
        d = {k: v for k, v in zip(L1, L2)}

        flag = False
        if d['Activities'] != 206 or d['ContactType'] != 101:
            flag=True
        for key in d:
            if d[key] is None: d[key] = ''
            if not key in dic: continue
            dic[key] = dic[key].strip()
            if dic[key] == d[key]: continue
            flag = True
            if dic[key] == '' :
                dic[key]=d[key]
                # print (key,'==',dic[key],'==',d[key])

        cursor.execute("select entryID from Domains_list where entryID=%s and Domain=%s limit 1;",(id,dom))
        if not cursor.fetchone():
            cursor.execute("insert into Domains_list (entryID,Domain) values ( %s , %s ); ",(id,dom))

        cursor.execute("select 1 from Comments where parID=%s and contents=%s limit 1;",(id,dic['comment']))
        if not cursor.fetchone():
            cursor.execute("insert into Comments (parID,contents) values (%s,%s);", (id, dic['comment']))

        if flag:
            cursor.execute('update Individual set FirstName = %s,LastName = %s,Email = %s,City = %s,'
                       'NewEntryDate=NOW(),'
                       'ContactType=101 ,0us_1him=1,Activities=206 where entryID =  %s;',
                       (
                           dic['fname'],
                           dic['name'],
                           dic['email'],
                           dic['city'],
                           id
                       ))
        db.commit()


# connnect()