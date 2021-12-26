import re

import MySQLdb
import pymysql
from MySQLdb._mysql import connect


def connect_db(DATABASE_NAME="smartcv"):
    try:
        # SERVER_NAME = "192.117.146.228"
        SERVER_NAME = "45.83.43.173"
        SERVER_USERNAME = "appdev"
        SERVER_PASSWORD = "Tengrinews1965"
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
    except MySQLdb.Error as e:
        print("ERROR::connect DB::", DATABASE_NAME, e)
        db = None
        exit(-1)
    return db, db.cursor()


# get all data from Individual by ID
# return dict
def get_Indiv(entry_i_d):
    db, cursor = connect_db()
    query = """ SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Individual' """
    cursor.execute(query)
    qdic = {}
    text = ''
    for key in cursor.fetchall():
        qdic[key[0]] = None
        text += str(key[0]) + ','
    text = text[:-1]
    cursor.execute("select " + text + " from Individual where entryID ={};".format(entry_i_d))
    ind = cursor.fetchall()[0]
    i = 0
    for key in qdic:
        qdic[key] = ind[i]
        i += 1
    db.close()
    return qdic


# prodact - domain
# get name if find return id
# else insert new return id
def get_domain_id(domain):
    db, cursor = connect_db()
    #  if domain exist
    domain = domain.replace('\n', '')
    domain = domain.replace('\r', '')
    domain = domain.replace('\'', '')
    domain = domain.replace('`', '')
    # domain = domain[:15]

    domain = domain.strip()
    dom = None
    if domain != '' and domain != ' ':
        if cursor.execute("select codeID from Domains where domain = %s;", (domain[:15],)) > 0:
            dom = cursor.fetchone()[0]
        else:
            cursor.execute("select codeID from Domains order by codeID desc limit 1;")
            dom = cursor.fetchone()[0] + 1
            cursor.execute('insert into Domains (codeID,domain) values ("%s",%s);', (dom, domain[:15]))
            db.commit()
    db.close()
    return dom, domain


def get_id_by_phone(phone):
    if len(phone) < 9: return None
    phone = phone[-9:]
    db, cursor = connect_db()
    id = None
    query = """
        select 
            entryID,Phone1,Phone2 
        from Individual 
        where Phone1 like %s or Phone2 like %s order by entryID desc;
    """
    if cursor.execute(query, ('%' + phone, '%' + phone)) > 0:
        id = cursor.fetchone()
    db.close()
    return id


def get_id_by_email(email):
    # print(re.findall(r'.+@\w+\.\w+', email))
    if len(email) <= 5: return
    db, cursor = connect_db()
    id = None
    query = "select entryID,Phone1,Phone2 from Individual where Email = %s ;"
    cursor.execute(query, (email,))
    id = cursor.fetchone()
    db.close()
    return id


def insert_new(FirstName, LastName, Phone1, Email, ContactType, location):
    db, cursor = connect_db()
    save_query = """
        INSERT INTO Individual
            (FirstName,LastName,Phone1,Email,ContactType,location,0us_1him,Activities) 
        VALUES(%s,     %s,      %s,      %s,   %s,         %s    ,   1,       200)
        ;"""
    cursor.execute(save_query, (FirstName, LastName, Phone1, Email, ContactType, location))
    db.commit()
    if cursor.execute(" select entryID from Individual where Email=%s and Phone1=%s ;", (Email, Phone1)) > 0:
        id = cursor.fetchone()
    else:
        id = None
    db.close()
    return id


def get_branch(city):
    ret = 100
    print("city  ", city)
    if 'haifa' in city or 'חיפה' in city:
        ret = 200
    elif 'rishon' in city or 'ראשון' in city:
        ret = 1
    print('city', ret)
    return ret


def set_to_db(dic):
    ### check telefon if is true
    # print(dic)
    if 'telefon' not in dic: return None
    if not dic['telefon']: return None
    dic['telefon'] = dic['telefon'].strip()
    if len(dic['telefon']) < 8:    return None
    if not dic['telefon'].isdigit():   return None
    if dic["telefon"] == '' or dic["telefon"] == ' ':        return None

    ### if domain exist
    dom, dic['domain'] = get_domain_id(dic['domain'])

    if 'tostudy' in dic['From']:
        dic['comment'] = "lid ToStudy: " + dic['domain']
    if 'tostudy' in dic['From']:
        dic['comment'] = "lid YORM: " + dic['comment']
    if 'rt-ed.co.il' in dic['From']:
        dic['comment'] = "lid info: " + dic['comment']

    id_t = get_id_by_phone(dic['telefon'])
    if id_t == None: id_t = get_id_by_email(dic["email"])
    if not id_t == None:
        id = id_t[0]
        print('found id ', id)
        if id_t[1][-9:] in dic['telefon']:
            dic['Phone1'] = id_t[1]
            dic['Phone2'] = id_t[2]
        else:
            dic['Phone2'] = id_t[1]
            dic['Phone1'] = dic['telefon']
    else:
        id = None
    dic["fname"] = dic["fname"][:15]
    dic["name"] = dic["name"][:15]
    dic['location'] = get_branch(dic["city"])
    db, cursor = connect_db()
    if not id:
        id = insert_new(dic["name"], dic["fname"], dic['telefon'], dic["email"], 101, dic['location'])
    else:
        cursor.execute(
            'select FirstName,LastName,Email,City,ContactType,Activities,location from Individual where entryID =  %s limit 1; ',
            (id,))
        L1 = ['fname', 'name', 'email', 'city', 'ContactType', 'Activities', 'location']
        L2 = cursor.fetchone()
        d = {k: v for k, v in zip(L1, L2)}
        flag = False
        if d['Activities'] != 206 or d['ContactType'] != 101:
            flag = True
        for key in d:
            if d[key] is None: d[key] = ''
            if not key in dic: continue
            dic[key] = str(dic[key]).strip()
            d[key] = str(d[key]).strip()
            if dic[key] == d[key]: continue
            flag = True
            if dic[key] == '':
                dic[key] = d[key]
                # print (key,'==',dic[key],'==',d[key])

        # cursor.execute("select entryID from Domains_list where entryID=%s and Domain=%s limit 1;", (id, dom))
        # if not cursor.fetchone():
        #     cursor.execute("insert into Domains_list (entryID,Domain) values ( %s , %s ); ", (id, dom))
        #
        # cursor.execute("select 1 from Comments where parID=%s and contents=%s limit 1;", (id, dic['comment']))
        # if not cursor.fetchone():
        #     cursor.execute("insert into Comments (parID,contents) values (%s,%s);", (id, dic['comment']))
        #
        # if flag:
        #     cursor.execute('update Individual set '
        #                    'FirstName = %s,'
        #                    'LastName = %s,'
        #                    'Email = %s, '
        #                    'NewEntryDate=NOW(),'
        #                    'ContactType=101 ,0us_1him=1,Activities=206, '
        #                    'Phone1=%s,Phone2=%s ,'
        #                    'location=%s'
        #                    'where entryID =  %s;',
        #                    (dic['fname'], dic['name'], dic['email'], dic["Phone1"], dic["Phone2"], dic["location"],
        #                     (id,)))
        # db.commit()
    db.close()
    return id


if __name__ == "__main__":
    print(get_Indiv(35))
    d = {}
    d["q"] = "`RT-Embedded`"
    n, d['q'] = get_domain_id(d["q"])
    print(n, d['q'])
    print(get_id_by_phone('0542082450'))
    print(get_id_by_email('@'))
