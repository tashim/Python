# python3
import pymysql
import MySQLdb  # mysql library
from datetime import datetime

import DB

db_name = 1

DATABASE_NAME = "smartcv"
# SERVER_NAME = "192.117.146.228"
SERVER_NAME = "45.83.43.173"
SERVER_USERNAME = "appdev"
SERVER_PASSWORD = "Tengrinews1965"


def db_connect():
    try:
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
    except MySQLdb.Error as e:
        print("error conn")
        db.rollback()
        print(e)
        exit(-1)
    # print(SERVER_NAME)
    return db


def get_Indiv(entryID):
    db = db_connect()
    query = """
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Individual'
"""
    coursor = db.cursor()
    coursor.execute(query)
    qdic = {}
    text = ''
    for key in coursor.fetchall():
        qdic[key[0]] = None
        text += str(key[0]) + ','
    text += 'Activities'

    # print(qdic)
    query = "select " + text + " from Individual where entryID ={};".format(entryID)
    # print(query)
    coursor.execute(query)
    ind = coursor.fetchall()[0]
    i = 0
    for key in qdic:
        qdic[key] = ind[i]
        i += 1
    db.close()
    print('ok=========================')
    return qdic


def set_to_db(dic):
    if not dic["telefon"] or dic["telefon"] == '' or dic["telefon"] == ' ':
        print('Not get telefon number')
        # return None
    db = db_connect()
    cursor = db.cursor()
    ### check telefon if is true
    dic['telefon'] = dic['telefon'].strip()
    dic['telefon'] = dic['telefon'].replace("+", "")
    dic['telefon'] = dic['telefon'].replace("-", "")
    dic['telefon'] = dic['telefon'].replace(" ", "")

    # if len(dic['telefon']) < 8:    return 0
    # dic['telefon'] = dic['telefon'].strip()
    # if not dic['telefon'].replace("+","").isdigit():   return 0
    #
    print('db:', dic)

    ### if domain exist
    dic['domain'] = dic['domain'].replace('\n', '')
    dic['domain'] = dic['domain'].replace('\r', '')
    dic['domain'] = dic['domain'].strip()
    dom = None
    if dic['domain'] != '' and dic['domain'] != ' ':
        dom = cursor.execute("select codeID from Domains where domain = %s;", dic['domain'])
        if dom:
            dom = cursor.fetchone()[0]
        else:
            cursor.execute("select codeID from Domains order by codeID desc limit 1;")
            dom = cursor.fetchone()[0] + 1
            cursor.execute('insert into Domains (codeID,domain) values ("%s",%s);', (dom, dic['domain']))
            db.commit()
    id = None
    query = "select entryID,Phone1,Phone2 from Individual where Phone1 like %s or Phone2 like %s limit 1;"
    get_query = None
    cursor.execute(query, ('%' + dic["telefon"][-9:], '%' + dic["telefon"][-9:]))
    get_query = cursor.fetchone()
    print(get_query)
    print('%' + dic["telefon"], '%' + dic["telefon"][-9:])
    if get_query:
        id = get_query[0]
        print('found id ', id, get_query[1], get_query[2])
        if get_query[1][-9:] in dic['telefon']:
            dic['Phone2'] = get_query[2]
            dic['Phone1'] = dic['telefon']
        else:
            dic['Phone1'] = get_query[1]
            dic['Phone2'] = dic['telefon']
    else:
        query = "select entryID,Phone1,Phone2 from Individual where Email like %s limit 1;"
        cursor.execute(query, dic["email"])
        get_query = cursor.fetchone()
        if get_query:
            id = get_query[0]
            dic['Phone2'] = get_query[1]
            dic['Phone1'] = dic['telefon']

        # print('not found id ', id, get_query[1], get_query[2])
    dic['location'] = DB.get_branch(dic["city"])
    print(dic)

    if not id:
        savequery = """
            INSERT INTO Individual
                (FirstName,LastName,Phone1,Email,ContactType,location,0us_1him,Activities) 
            VALUES(%s,         %s,     %s,     %s,     %s,         %s,     1,      200)
            ;"""
        cursor.execute(savequery,
                       (dic["name"],
                        dic["fname"],
                        dic["telefon"],
                        dic["email"],
                        dic["ContactType"],
                        dic['location']))
        db.commit()
        #   Get his ID
        if cursor.execute("Select entryID from Individual where Phone1=%s;", (dic["telefon"],)):
            id = cursor.fetchone()[0]
        dic['Phone2'] = ''
        dic['Phone1'] = dic['telefon']
        db.commit()
    else:
        cursor.execute('update Individual set FirstName = %s,LastName = %s,Email = %s,location = %s,'
                       'NewEntryDate=NOW(), Phone1 = %s, Phone2 = %s, ContactType=%s ,0us_1him=1 where entryID =  %s;',
                       (dic['fname'], dic['name'], dic['email'], dic['location'],
                        dic['Phone1'], dic['Phone1'], dic['ContactType'], id))
        db.commit()

    if id:
        cursor.execute("select entryID from Domains_list where entryID=%s and Domain=%s limit 1;", (id, dom))
        if not cursor.fetchone():
            cursor.execute("insert into Domains_list (entryID,Domain) values ( %s , %s ); ", (id, dom))
            print('insert domain list')

        cursor.execute("select 1 from Comments where parID=%s and contents=%s limit 1;", (id, dic['comment']))
        if not cursor.fetchone():
            cursor.execute("insert into Comments (parID,contents) values (%s,%s);", (id, dic['comment']))
            print('insert comment')
        db.commit()
    dic['entryID'] = id
    db.close()
    return id
# connnect()
