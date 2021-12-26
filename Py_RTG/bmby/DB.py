
import MySQLdb  # mysql library

import pymysql

from test import log
db_name = 1
if db_name == None:
    SERVER_NAME = "localhost"
    SERVER_USERNAME = "root"
    SERVER_PASSWORD = "1234"
elif db_name == 0:
    SERVER_NAME = '192.168.1.63'
    SERVER_USERNAME = 'vadim'
    SERVER_PASSWORD = '!1+=2018Y'
elif db_name == 1:
    SERVER_NAME = "45.83.43.173"
    SERVER_USERNAME = "appdev"
    SERVER_PASSWORD = "Tengrinews1965"

DATABASE_NAME_STUD = "studentsTest2"
DATABASE_NAME_SMART = "smartcv"
dbst = dbsm = 0

def con_close(db):
    db.cursor.close()
    db.close()

def connnect(DATABASE_NAME):
    try:
        print(SERVER_NAME)
        # print(SERVER_USERNAME)
        # print(SERVER_PASSWORD)
        print(DATABASE_NAME)
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
        return db
    except MySQLdb.Error as e:
        print("error conn")
        print (e)
        return  0

# Open connection to DB
# try:
    # dbst = connnect(DATABASE_NAME_STUD)
dbsm = connnect(DATABASE_NAME_SMART)
# except:
#     print("error connect ", end=" ")
#     print(DATABASE_NAME_SMART)
#     exit(-1)

def find_in_sm(tel):
    cur = dbsm.cursor()

    try:
        cur = dbsm.cursor()
        n = cur.execute(
            """
       SHOW
    columns 
    FROM
    Individual;

            """
            )
    except MemoryError as e:
        print(e)
    keys =  [column[0] for column in  cur.fetchall()]
    # print(keys )
    try:
         n = cur.execute("SELECT * FROM Individual where Phone1 like '%"+tel+"' or Phone2 like '%"+tel+"';")
    except MemoryError as e:
        print(e)
    ret =[]
    for d in cur.fetchall():    ret.append(dict(zip(keys,d)))
    return n,ret

# TODO get person ID
#  get list [ email, tel1,tel2 ]  and update it if need
# return list entryID , tel_list
def get_person_Id(tel_list):
    tel = tel_list.copy()
    entryID = []
    while len(tel_list)< 3:
        tel_list.append("X_no_data_X")
    if tel_list[1] == tel_list[2]: tel_list[2]="X_no_data_X"
    try:
        t = int(str(tel_list[1])[-9:])
        if len(str(t))<3:tel_list[1]="X_no_data_X"
    except:
        pass
    try:
        t = int(str(tel_list[2])[-9:])
        if len(str(t))<3:tel_list[2]="X_no_data_X"
    except:
        pass

    # print(tel_list)
    if len(tel_list[0]) < 3 : tel_list[0]="X_no_data_X"
    cur = dbsm.cursor()
    s = "SELECT entryID,Email,Phone1,Phone2 FROM Individual where "\
        " Phone1 in " + str(tuple(tel_list)) +\
        " OR Email in " + str(tuple(tel_list))
    for i in range(1,len(tel_list)):
        if tel_list[i] != "X_no_data_X":
            # print(str(tel_list[i])[-9:])
            # print(len(str(tel_list[i])[-9:]))
            if len(str(tel_list[i])[-9:])<8 :continue
            s+=" OR Phone1 like '%"+str(tel_list[i])[-9:] +"' "
            s+=" OR Phone2 like '%"+str(tel_list[i])[-9:] +"' "
    s+= " OR Phone2 in " + str(tuple(tel_list)) + " order by entryID desc;"
    # print(s)
    # return None
    n = cur.execute(s)
    if n == 0 :return tel,None
    while len(tel)<3:   tel.append('')
    for record in cur.fetchall():
        entryID.append(record[0])
        rec=[]
        for i in record:
            # print(i)
            if not i : rec.append('')
            else:
                si = str(i).replace("-",'')
                si = si.replace("\n",'')
                rec.append(str(i))

        if len(tel[0]) < 5: tel[0] = rec[1]
        if not tel[1] or len(tel[1]) < 5:
            if len(rec[2]) > 5:
                tel[1] = rec[2]
            else:
                if len(rec[3]) > 5:
                    tel[1] = rec[3]
                else: continue
        if tel[2] == tel[1]:tel[2] = ""
        if not tel[1] or len(tel[1]) < 5: continue
        if not tel[2] or len(tel[2]) < 5:
            if len(rec[2]) > 5 :
                if not rec[2] in tel: tel[2] = rec[2]
        if not tel[2] or len(tel[2]) < 5:
            if len(rec[3]) > 5 :
                if not rec[3] in tel: tel[2] = rec[3]
    return tel,entryID

# #Todo Update Smart
def get_media_ID_SM(s_media):
    # select from media
    if len(s_media)>20: s_media = s_media[:20]
    cur = dbsm.cursor()
    n = cur.execute("SELECT codeID FROM ContactTypes WHERE type='" + s_media + "';")
    if n > 0 :
        return cur.fetchone()[0]
    # if not
    #   add new record
    else:
        cur.execute("SELECT max(codeID) FROM ContactTypes ;")
        int_media = cur.fetchone()[0]+1
        cur.execute("INSERT INTO `ContactTypes` (`codeID`, `type`) VALUES ('"+str(int_media)+"', '"+s_media+"');")
        dbsm.commit()
        return int_media
    #

#todo Update Status in SmartCV
def get_status_id(s_status):
    # find if exist
    cur = dbsm.cursor()
    n = cur.execute("SELECT codeID FROM Activities WHERE type='" + s_status + "';")
    if n > 0 :
        return cur.fetchone()[0]
    # if not
    #   add new record
    else:
        cur.execute("SELECT max(codeID) FROM Activities ;")
        int_status = cur.fetchone()[0]+1
        cur.execute("INSERT INTO `Activities` (`codeID`, `type`) VALUES ('"+str(int_status)+"', '"+s_status+"');")
        dbsm.commit()
        return int_status
    #

def get_relevant_id(relvant,s_status):
    # find if exist
    if relvant == 0:        return 0
    if s_status == '' :     return 1
    cur = dbsm.cursor()
    n = cur.execute("SELECT idrelevant FROM relevant WHERE relevant_text='" + s_status + "';")
    if n > 0 :
        return cur.fetchone()[0]
    # if not
    #   add new record
    else:
        cur.execute("SELECT max(idrelevant) FROM relevant ;")
        int_status = cur.fetchone()[0]+1
        cur.execute("INSERT INTO `relevant` (`idrelevant`, `relevant_text`) VALUES ('"+str(int_status)+"', '"+s_status+"');")
        dbsm.commit()
        return int_status
    #

#todo Update Company in SmartCV
def get_company_id(s_name):
    # find if exist
    if s_name == '':return 0
    cur = dbsm.cursor()
    n = cur.execute("SELECT nameID FROM companyNames WHERE name='" + s_name + "';")
    if n > 0 :
        return cur.fetchone()[0]
    # if not
    #   add new record
    else:
        cur.execute("SELECT max(nameID) FROM companyNames ;")
        int_name = cur.fetchone()[0]+1
        cur.execute("INSERT INTO `companyNames` (`nameID`, `name`) VALUES ('"+str(int_name)+"', '"+s_name+"');")
        dbsm.commit()
        return int_name
    #
#todo Update User in SmartCV
def get_user_id(s_name):
    # find if exist
    if s_name == '':return 0
    cur = dbsm.cursor()
    n = cur.execute("SELECT userid FROM users WHERE user_full_name='" + s_name + "';")
    if n > 0 :
        return cur.fetchone()[0]
    else:
        cur.execute("SELECT max(userid) FROM users ;")
        int_name = cur.fetchone()[0]+1
        s_fname = s_name
        s_name = s_name.split()[0]
        q = "INSERT INTO `users` (`userid`, `username`, `user_full_name`,pass) VALUES ('"+str(int_name)+"', '"+s_name+"', '"+s_fname+"','1');"
        print(q)
        cur.execute(q)
        dbsm.commit()
        return int_name

    return  1


#Todo Update Smart
def smart_update(data):
    pass
    #Todo Get media ID
    #Todo Update
    #Todo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Update DB smartCV on double Phone number
def Updete_Sm_for_Double():
#     find double phone
    if 1:
        command = """
    SELECT
           GROUP_CONCAT(entryID)
        FROM
            Individual
             where LENGTH(Phone1) > 5

        GROUP BY Phone1
        HAVING COUNT(*) > 1 ; """
    elif 1:
        command =    """
        SELECT
               GROUP_CONCAT(entryID)
            FROM
                Individual
                 where  locate('@', Email) > 3
    
            GROUP BY Email
            HAVING COUNT(*) > 1 ;
          """
    else:
        command = """SELECT entryID,Phone1,Phone2,Email FROM smartcv.Individual where 
        b_entryID =0
        """

    cur = dbsm.cursor()

    print(command)
    coutnt=cur.execute(command)
    rezu = cur.fetchall()
    print(coutnt)
    print(rezu)
    for r in rezu:
        l=[]
        print(r)
        for i in r[0].split(','): l.append(i)
        print(len(l),l)
        Updete_Double(l)
    return None
    l = 0

    for r in rezu:
        r = list(r)
        if r[1]:r[1] = str(r[1]).replace('-','')
        if r[1]:r[1] = str(r[1]).replace(' ','')
        if r[2]:r[2] = str(r[2]).replace('-','')
        if r[2]:r[2] = str(r[2]).replace(' ','')
        if r[0]:r[0] = str(r[0]).replace(' ','')
        if (r[1] ==  None or len(r[1])<5) and   (r[2] == None or len(r[2]) < 5):
            pass
        else:
            if not(r[1] ==  None or len(r[1])<9 ):
                # print(len(r[1]),r[1])
                s = """
            SELECT entryID FROM Individual WHERE 
            """

                s += " Phone1 like '%" + r[1][len(r[1])-9:] + "'"
                s += " or Phone2 like '%" + r[1][len(r[1])-9:] + "';"

                cur = dbsm.cursor()
                x = cur.execute(s)
                if x > 1:
                    l +=1
                    print(l,x)
                    li = []
                    for i in cur.fetchall():  li.append(i[0])
                    Updete_Double(li)
                    print(li)

    return  None
    for r in rezu:
        # print(r)
        r = r[0]
        r.replace("'","")
        r.replace("'","")
        r.replace("'","")
        r.replace("`","")
        mlist = []
        max = 0
        for l in r.split(","):
            if (int(l)>max):
                max =int(l)
                mlist.insert(0,l)
            else:
                mlist.append(l)
        print(mlist[0])
    return  None

 # Update DB smartCV on double Phone number by list
#
def Updete_Double(entrys):
    print(entrys)
    print(type(entrys))
    if len(entrys) < 2: return None
    print(len(entrys))
    max = int(entrys[0])
    for l in entrys:
        if (int(l)>max):
            max =int(l)
    max = str(max)
    print(str(max))
    print("entrys == ",entrys)

    e=''
    for i in range(0,len(entrys)): e +=str(entrys[i]) +','
    e=e[:-1]
    items =['b_entryID','FirstName',
            'LastName','Phone1','Phone2','CV','Email', \
            'Address','City','file_path' ]
    s = "select "
    for i in range(0,len(items)-1):
        s+= items[i]+","
    s+= items[-1]+" "
    s +=" from Individual " \
        " where entryID in ( "+e+" ) order by entryID desc;"
    print(s)
    print(max)
    cur = dbsm.cursor()
    cur.execute(s)
    rez = []
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    for r in cur.fetchall():
        rez.append(dict(zip(items,r)))
        print(dict(zip(items,r)))

    if len(rez) < 2: return None
    rez_d = rez[0].copy()
    for rp in rez:
        for i in rp:
            if i == 'b_entryID':
                if rez_d[i] == 0: rez_d[i] = rp[i]
            elif rez_d[i] == None or rez_d[i]=='None' or rez_d[i] in ('','לא ידוע'):
                rez_d[i]= rp[i]
                if rp[i] == None or str(rp[i])=='None' or rez_d[i] in ('','לא ידוע'):
                    rez_d[i]=''
                rez_d[i]=str(rez_d[i]).replace("'"," ")
                rez_d[i]=str(rez_d[i]).replace("`"," ")
                rez_d[i]=str(rez_d[i]).replace("'"," ")
    print( "p=",rez[0])

    print( "rez_d=",rez_d)

    # TODO Update table Calls parID to max entryID
    mlist = entrys.copy()
    mlist.remove(int(max))
    print('e>',entrys)
    print('m>',mlist)
    s = """
        UPDATE calls SET
        parID='""" + str(max)  +"""'
        WHERE parID in """+str(tuple(mlist)+('-111',)) + ';'
    cur.execute(s)
    print(mlist)
    print(s)


    # TODO Update table Comments parID to max entryID
    s = """
        UPDATE Comments SET
        parID='""" + str(max)  +"""'
        WHERE parID in """+str(tuple(mlist)+('-111',)) + ';'
    print(mlist)
    print(s)

    cur.execute(s)
    # TODO Update table Domains_list entryID to max entryID
    s = """
        UPDATE Domains_list SET
        entryID = '""" + str(max)  +"""'
        WHERE entryID in """+str(tuple(mlist)+('-111',)) + ';'
    print(mlist)
    print(s)
    cur.execute(s)
    # TODO Update table Education parID to max entryID
    s = """
        UPDATE Education SET
        parID = '""" + str(max)  +"""'
        WHERE parID in """+\
        str(tuple(mlist)+('-111',)) + ' order by parID desc limit 1;'
    print(mlist)
    print(s)
    cur.execute(s)
    #       delete other entry
    s = """
        DELETE FROM Education WHERE parID in """ + \
        str(tuple(mlist)+('-111',)) + ';'
    print(mlist[1:])
    print(s)
    cur.execute(s)

    # TODO Update table experience parID to max entryID
    s = """
         UPDATE Experience SET
         parID = '""" + str(max) + """'
         WHERE parID in """ + \
        str(tuple(mlist) + ('-111',)) + ' order by parID desc limit 1;'
    print(mlist)
    print(s)
    cur.execute(s)
    #       delete other entry
    s = """
         DELETE FROM Experience WHERE parID in """ + \
        str(tuple(mlist) + ('-111',)) + ';'
    print(s)
    cur.execute(s)
    # TODO Update table Indiv_status parID to max entryID
    # TODO Update table Skills
    s = """
        UPDATE Skills SET
        parID = '""" + str(max)  +"""'
        WHERE parID in """+\
        str(tuple(mlist)+('-111',)) + ' order by parID desc limit 1;'
    print(s)
    cur.execute(s)
    #       delete other entry
    s = """
        DELETE FROM Skills WHERE parID in """ + \
        str(tuple(mlist)+('-111',)) + ';'
    print(s)

    # TODO Update table TestGrade
    #       delete other entry
    s = """
        DELETE FROM testGrade WHERE parID in """ + \
        str(tuple(mlist)+('-111',)) + ';'
    print(s)
    cur.execute(s)
    s = """
        UPDATE testGrade SET
        parID = '""" + str(max)  +"""'
        WHERE parID in """+\
        str(tuple(mlist)+('-111',)) + ' order by parID desc limit 1;'
    print(s)
    cur.execute(s)
    # TODO MeetingDate
    s = """
         UPDATE MeetingsDate SET
         parID = '""" + str(max) + """'
         WHERE parID in """ + \
        str(tuple(mlist) + ('-111',)) + ';'
    print(s)
    cur.execute(s)

    # TODO Update max entryID
    if (rez_d['Phone1']==''):rez_d['Phone1']='null'
    if (rez_d['Phone2']==''):rez_d['Phone2']='null'
    s = " UPDATE Individual SET "
    for i in rez_d:
        try:
            rez_d[i] = rez_d[i].replace("'",'')
            rez_d[i] = rez_d[i].replace("`",'')
            rez_d[i] = rez_d[i].replace(" ",'')
        except:
            pass
        if rez_d == 'null':
            s += " " + i+"="+str(rez_d[i]) + "  ,"
        else:
            s += " " + i +"='"+ str(rez_d[i]) + "'  ,"
    s = s[:-1]
    s += "WHERE entryID = """+str(max) + ';'
    print(s)
    cur.execute(s)

    # TODO Delete other entry
    s = """
    DELETE FROM Individual WHERE entryID in """+str(tuple(mlist)+('0',)) + ';'
    cur.execute(s)
    print("error == =",cur.Error())

    # coutnt = coutnt +1
    dbsm.commit()
    #
    # print(coutnt)

def get_user(usr):
    try:
        usr = int(usr)
    except:
        return 0
    sm_user = [500,     503,    507,    508,    102,    101]
    bm_user = [45599,   45575,  45557,  45804,  45526,  45725]
    if not usr in bm_user: return usr
    return  sm_user[bm_user.index(usr)]

#Todo udate task
def task_update(dic):
    lisr_d = ["task_id",'media_id','type','client_id','subject','message',
              'location','status','start_date','due_date','priority',
              'create_user_id','update_user_id','create_date','update_date',
              'user_id']
    dic["user_id"] = get_user(dic["user_id"])
    dic["create_user_id"] = get_user(dic["create_user_id"])
    dic["update_user_id"] = get_user(dic["update_user_id"])

    # print(dic['subject'])
    for i in lisr_d:
        if type(dic[i]) is type(str()):
            dic[i] = dic[i].replace("'","`")
            # print(dic[i])
    s="insert into tasks ("
    for l in lisr_d:
        s+=l+","
    s = s[:-1]+") values ("
    for l in lisr_d:
        if dic[l]:
            s+="'"+str(dic[l])+"',"
        else:
            s+="null,"
    s = s[:-1]+") on duplicate key update "
    for l in lisr_d:
        s += "{0}=values({0}),".format(l)
    s = s[:-1]+";"
    # print(s)
    cur = dbsm.cursor()
    cur.execute(s)
    dbsm.commit()

    try:
        cur = dbsm.cursor()
        cur.execute(s)
        dbsm.commit()
        return 0
    except MySQLdb.Error as e:
        log(e)
        print(e)
        return  -1
    except:
        print(s)
        log(s)
        return -2