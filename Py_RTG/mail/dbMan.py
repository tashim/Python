
import pymysql
import MySQLdb  # mysql library
from datetime import datetime

#
# SERVER_USERNAME = "vadim"
# SERVER_PASSWORD = "!1+=2018Y"
# SERVER_NAME = "192.168.1.63"
import DB


def set_to_db(dic,db_name=None):
    ### check telefon if is true
    if 'telefon' not in dic: return  None
    if not dic['telefon']: return  None
    dic['telefon'] = dic['telefon'].strip()
    if len(dic['telefon']) < 8:    return None
    if not dic['telefon'].isdigit():   return None
    if dic["telefon"] == '' or dic["telefon"] == ' ' :        return None

    DATABASE_NAME = "smartcv"
    SERVER_NAME = "45.83.43.173"
    SERVER_USERNAME = "appdev"
    SERVER_PASSWORD = "Tengrinews1965"
    try:
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
    except MySQLdb.Error as e:
        print (e)
        exit(-1)
    cursor = db.cursor()

### if domain exist
    dic['domain'] = dic['domain'].replace('\n','')
    dic['domain'] = dic['domain'].replace('\r','')
    dic['domain'] = dic['domain'].replace('\'','')
    dic['domain'] = dic['domain'].replace('`','')
    dic['domain'] = dic['domain'].strip()
    if len(dic['domain'])>15: dic['domain'] = dic['domain'][:15]

    dom = None
    if dic['domain'] != '' and dic['domain'] != ' ':
        q = "select codeID from Domains where '"+dic['domain'][:10]+"%' like domain"
        dom = 0
        if cursor.execute(q)>0:
            dom = cursor.fetchone()[0]
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
        dic['comment'] = "lid info: " + dic['comment']
    id = None

    query = "select entryID,Phone1,Phone2 from Individual where Phone1 like %s or Phone2 like %s limit 1;"
    get_query = None
    cursor.execute(query, ('%' + dic["telefon"][-9:], '%' + dic["telefon"][-9:]))
    get_query = cursor.fetchone()
    if get_query:
        id = get_query[0]
        print('found id ', id, get_query[1], get_query[2])
        dic['Phone1'] = dic['telefon']
        if get_query[1][-9:] in dic['telefon']: dic['Phone2'] = get_query[2]
        else:                                   dic['Phone2'] = get_query[1]
    elif  len(dic["email"])>5:
        query = "select entryID,Phone1,Phone2 from Individual where Email like %s limit 1;"
        cursor.execute(query, dic["email"])
        get_query = cursor.fetchone()
        if get_query:
            id = get_query[0]
            dic['Phone2'] = get_query[1]
            dic['Phone1'] = dic['telefon']

    dic['location'] = DB.get_branch(dic["city"])
    if not id:
        try:
### insert new entry

            savequery = "INSERT INTO Individual(FirstName,LastName,Phone1,Email,ContactType,City,0us_1him,Activities)" \
                        "VALUES(                %s,         %s,     %s,     %s,  101,%s,1,200);"
            cursor.execute(savequery,(dic["name"],dic["fname"],dic["telefon"],dic["email"],dic['location']))
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
        cursor.execute('select FirstName,LastName,Email,City,ContactType,Activities from Individual where entryID =  %s limit 1; ',id)
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
            cursor.execute( 'update Individual set FirstName = %s,LastName = %s,Email = %s, NewEntryDate=NOW(),'
                       'ContactType=101 ,0us_1him=1,Activities=206, Phone1=%s,Phone2=%s '
                            'where entryID =  %s;',
                       ( dic['fname'], dic['name'], dic['email'], dic["Phone1"],dic["Phone2"], id  ) )
        db.commit()
    return id
    db.close()


def is_student(phone):
    ### check telefon if is true
    if not phone: return  None
    phone = phone.strip()
    if len(phone) < 8:    return None
    if not phone.isdigit():   return None
    if phone == '' or phone == ' ' :        return None

    DATABASE_NAME = "studentsTest2"
    SERVER_NAME = "45.83.43.173"
    SERVER_USERNAME = "appdev"
    SERVER_PASSWORD = "Tengrinews1965"
    try:
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
    except MySQLdb.Error as e:
        print("error conn")
        db.rollback()
        print (e)
        exit(-1)
    cursor = db.cursor()
    cursor.execute("SELECT studentID FROM students where mobileNumber like %s;",
                   ('%'+phone[-9:],))
    ret = cursor.fetchone()
    if ret :
        ret = ret[0]
        cursor.execute("INSERT INTO in_calls (phone,studentID) VALUES (%s, %s);",(phone,ret))
        db.commit()
    else: ret = 0
    print(ret)
    db.close()
    return ret
# connnect()