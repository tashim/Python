import json

import zeep
from zeep import helpers

from DB import *
# wsdl = 'https://bmby.com/WebServices/srv/v3/tasks.php?wsdl'
from test import log

wsdl = 'https://bmby.com/WebServices/srv/clients.php?wsdl'
client = zeep.Client(wsdl=wsdl)
data = {}
data['Login'] = 'rtgroup'
data['Password'] = '051218'
data['ProjectID'] = '8056'
data['ContractID'] = ""
data['OrderDesc'] = 0
data['Type'] = ''
data['TaskID'] = ''
data['UniqID'] = ''
# data['LastUniqID'] =   '1111111111'
data['LastUniqID'] = ' '
# data['ClientID'] = 1113446925
data['ClientID'] = 0
data['ToDate'] = ''
# data['ToDate'] = '2018-10-08'
data['Dynamic'] = 0
data['FromDate'] = '2018-10-08'
# data['FromDate'] = ''
data['Limit'] = '1000'
# data['SetPrivate'] = '1'
data['OwnerID'] = ''
data['Offset'] = ''
data['TypeString'] = ''


# result = client.service.GetAll(data)
# print(json.loads(result))
def GetData():
    # global  count,last
    count = 0
    last = 0
    # todo TRY EXEPTION
    rez = client.service.GetAll(data)
    ret = helpers.serialize_object(rez)
    j = json.loads(json.dumps(ret))
    rez_list = []
    count = j["FoundRows"]
    print(count)
    if j["FoundRows"] > 0:
        last = j["LastUniqID"]
        if (data):
            l = j["Data"].split("<row>")
        else:
            l = None
        list = []
        if l:
            for x in range(1, len(l)):
                l[x] = l[x].split("\n")
                if (len(l[x]) > 0):
                    dic = {}
                    for i in range(0, len(l[x])):
                        l[x][i] = l[x][i].split("</")[0]
                        l[x][i] = l[x][i].replace(">", "#")
                        l[x][i] = l[x][i].replace("<", "")
                        l[x][i] = l[x][i].replace("##", "&")
                        l[x][i] = l[x][i].replace("![CDATA[", "")
                        l[x][i] = l[x][i].replace("]]", "")
                        ls = l[x][i].split("#")
                        if (len(ls) > 1):
                            dic[ls[0]] = ls[1].replace("'", "`")
                    rez_list.append(dic)
    return (count, last, rez_list)
    # return j["LastUniqID"]


if __name__ == '__main__':

    data['UniqID'] = '1113341490'
    data['UniqID'] = '1112000000'
    # data['UniqID'] = '1113411240'
    # data['UniqID'] = '1113527970'
    log("update all " + SERVER_NAME)
    insert = 0
    update = 0
    delete = 0
    c = 0
    list = []
    user = []
    us_ud = []
    while 1:
        count, last, rez = GetData()
        # for  f in rez:
        #     for i in f:
        #         if str(f[i]) in ('0','0'):
        #             print(i,f[i])
        # # exit(1)
        log("  last " + str(last) + " | " + str(data['UniqID']) + " | " + str(count))
        print(last, "|", c)
        # continue
        for r in rez:
            if "phone_mobile" in r:
                c += 1
                tel = []
                tel.append(r["email"])
                if (len(r["phone_mobile"]) > 3):
                    tel.append(r["phone_mobile"])
                if (len(r["phone_home"]) > 3):
                    tel.append(r["phone_home"])
                if (len(r["phone_work"]) > 3):
                    tel.append(r["phone_work"])
                # if len(r["email"]) <3:
                # print(tel)
                t, e = get_person_Id(tel.copy())

                if e:
                    update += 1
                    if len(e) > 1:
                        delete += len(e[1:])
                        log(str(delete) + "  delete " + str(e) + " cl_id " + str(r["client_id"]))
                        print("delete", delete, e[1:])
                    print("update ", update, e[0], e)
                    # continue
                    s = """ UPDATE Individual SET  """
                    s += "gender ='" + r["gender"] + "'"
                    if r["client_date"] != '':
                        s += ",EntryDate ='" + r["client_date"] + "'"
                    if r["client_id"] != '':
                        s += ",b_entryID ='" + str(r["client_id"]) + "'"
                    if r["fname"] != '':
                        s += ",FirstName ='" + r["fname"] + "'"
                    if r["lname"] != '':
                        s += ",LastName ='" + r["lname"] + "'"
                    if r["passport"] != '':
                        s += ",personID ='" + r["passport"] + "'"
                    if len(t) >= 2 and t[1] != '':
                        s += ",Phone1 ='" + str(t[1]) + "'"
                    if len(t) >= 3 and t[2] != '':
                        s += ",Phone2 ='" + t[2] + "'"
                    if t[0] != '':
                        s += ",Email ='" + t[0] + "'"
                    if r["birth_day"] != '':
                        s += ",DateOfBirth ='" + r["birth_day"] + "'"
                    if r["city"] != '':
                        s += ",City ='" + r["city"] + "'"
                    if r["address"] != '':
                        s += ",Address ='" + r["address"] + "'"
                    if r["media"] != "":
                        s += ",ContactType ='" + str(get_media_ID_SM(r["media"])) + "'"

                    if r["user_name"] != '':
                        s += ",TaskOf ='" + str(get_user_id(r["user_name"])) + "'"

                    status = get_status_id(r["status"])
                    if r["status"] != '':
                        s += ",Activities ='" + str(status) + "'"

                    if status == 219: r["relevant"] = 0
                    allowSMS = '1'
                    if status == 201: allowSMS = '0'
                    s += ",allowed_sms ='" + allowSMS + "'"
                    s += ",relevant ='" + str(get_relevant_id(r["relevant"], r["seriousness"])) + "'"
                    s += ",company_id ='" + str(get_company_id(r["company_name"])) + "'"
                    s += "where entryID='" + str(e[0]) + "';"
                    # print(s)
                    try:
                        cur = dbsm.cursor()
                        cur.execute(s)
                        dbsm.commit()
                    except:
                        print(s)
                        log(str(dbsm.Error) + "\n" + s)

                    if len(e) > 1:
                        delete += len(e[1:])
                        log(str(delete) + "  delete " + str(e) + " cl_id " + str(r["client_id"]))
                        Updete_Double(e)
                        print("delete", delete, e)
                else:
                    s = """
                    INSERT INTO Individual
                    (   EntryDate,
                        FirstName,
                        LastName,
                        personID,
                        Phone1,
                        Phone2,
                        Email,
                        DateOfBirth,
                        City,
                        Address,
                        ContactType,
                        TaskOf,
                        Activities,
                        
                        allowed_sms,
                        gender,
                        relevant,
                        company_id,
                        b_entryID
                    )
                    
                    VALUES(
                    """
                    s += "'" + r["client_date"] + "',"
                    s += "'" + r["fname"] + "',"
                    s += "'" + r["lname"] + "',"
                    s += "'" + r["passport"] + "',"
                    if len(t) < 2:
                        s += "'',"
                    else:
                        s += "'" + t[1] + "',"
                    if len(t) < 3:
                        s += "null,"
                    else:
                        s += "'" + t[2] + "',"
                    s += "'" + t[0] + "',"
                    s += "'" + r["birth_day"] + "',"
                    s += "'" + r["city"] + "',"
                    s += "'" + r["address"] + "',"
                    s += "'" + str(get_media_ID_SM(r["media"])) + "',"
                    s += "'" + str(get_user_id(r["user_name"])) + "',"
                    status = get_status_id(r["status"])
                    s += "'" + str(status) + "',"

                    if status == 219: r["relevant"] = 0
                    allowSMS = '1'
                    if status == 201: allowSMS = '0'
                    s += "'" + allowSMS + "',"
                    s += "'" + str(r["gender"]) + "',"
                    s += "'" + str(get_relevant_id(r["relevant"], r["seriousness"])) + "',"
                    s += "'" + str(get_company_id(r["company_name"])) + "',"
                    s += "'" + str(r["client_id"]) + "'"
                    s += ");"

                    # print("INSERT",r)
                    try:
                        cur = dbsm.cursor()
                        cur.execute(s)
                        dbsm.commit()
                    except:
                        log(str(dbsm.Error) + "\n" + s)
                    insert += 1
                    log("  " + str(insert) + " " + str(insert) + str(t) + " cl " + str(r["client_id"]))
                    print(insert, t)

        if 0 == last:
            break
        else:
            data['UniqID'] = last
        # print()
    print("ins=", insert)
    print("upd=", update)
    print("del=", delete)
    print(c)
    for i in range(0, len(user)):
        print(user[i], us_ud[i])

"""    
    last ="1113006477"
    while str(last) != '0' :

        data['UniqID'] = last
        # data['ClientID'] -= 1

        last = GetData(data)

    print(count,"=end=")
"""
