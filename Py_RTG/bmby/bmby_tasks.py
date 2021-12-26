import json
import os
import signal
from datetime import datetime

# import suds
import zeep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers import cron

from future.backports.datetime import timedelta
from suds import WebFault
from zeep import helpers

from socket import timeout

from DB import task_update
from test import log

wsdl = 'https://bmby.com/WebServices/srv/v3/tasks.php?wsdl'
# wsdl = 'https://bmby.com/WebServices/srv/clients.php?wsdl'
client = zeep.Client(wsdl=wsdl)
# client.set_options(timeout=10)
data = {}
data['Login'] = 'rtgroup'
data['Password'] = '051218'
data['ProjectID'] = '8056'
data['ContractID'] = ""
data['OrderDesc'] = ''
data['Type'] = ''
data['TaskID'] = ''
data['UniqID'] = ''
data['LastUniqID'] = ''
data['ClientID'] = ''
data['ToDate'] = ''
data['Dynamic'] = ''
data['FromDate'] = ''
data['Limit'] = 10
data['SetPrivate'] = ''
data['OwnerID'] = ''
data['Offset'] = ''
data['TypeString'] = ''

all=0
data['UniqID'] = ''
global safe
safe = datetime.now()
StartDate =  datetime.strptime("01/01/19", "%d/%m/%y")
# StartDate =  datetime.now()+timedelta(days=-1)
# StartDate =  datetime.now()-timedelta(days=2)
EndDate = StartDate + timedelta(days=2)
data['FromDate'] = StartDate.strftime("%Y-%m-%d")
data['ToDate'] = EndDate.strftime("%Y-%m-%d")
log("start from date:"+data['FromDate'])
#
# def check():
#     global safe
#     print(safe)
#     if safe:
#         # # print("===============================================================================")
#         # print(safe)
#         # print((datetime.now()-safe).seconds )
#         if (datetime.now()-safe).seconds > 60:
#             log("error timeout"+safe.strftime("%H:%M:S"))
#             os.kill(os.getpid(), signal.SIGTERM)
#
# scheduler = BackgroundScheduler()
# scheduler.start()
#
# trigger = cron.CronTrigger( second='*/10')
# scheduler.add_job(check, trigger=trigger)

while (StartDate - datetime.now()).days <=0 :
    try:
        print('STD:',StartDate,(StartDate - datetime.now()).days )
        # print("read from BMBY")
        safe = datetime.now()
        rez = client.service.GetAll(data)
        # input()
        safe = None
        # print("read from call BMBY")
        ret = helpers.serialize_object(rez)
        j = json.loads(json.dumps(ret))
        if data["Limit"] <= 100 and int(j["FoundRows"]) > 0:
            data["Limit"] *= 10
            # print("limit * 2 :",data["Limit"])
            # print(j["FoundRows"])
    except WebFault as detail:
        print(detail)
    except:
        if data['Limit'] <=1:
            # print(StartDate,"<<<exept>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            StartDate = StartDate + timedelta(days=1)
            EndDate = StartDate + timedelta(days=2)
            data['FromDate'] = StartDate.strftime("%Y-%m-%d")
            data['ToDate'] = EndDate.strftime("%Y-%m-%d")
            data['UniqID'] = ''
            continue
        else:
            data['Limit'] =int (data['Limit'] /10)
            if data["Limit"]==0: data["Limit"] = 1
            print("limit",data['Limit'] )
            continue
    if j["FoundRows"]==0 :
        # print(StartDate, EndDate,"<<<was>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        StartDate = StartDate + timedelta(days=1)
        EndDate = StartDate + timedelta(days=2)
        # print(StartDate, EndDate,"<<<new>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        data['FromDate'] = StartDate.strftime("%Y-%m-%d")
        data['ToDate'] = EndDate.strftime("%Y-%m-%d")
        data['UniqID'] = ''
        continue
    print(data['FromDate'],data['ToDate'])
    # print(data['UniqID'],"++++++")
    # print(data['Limit'])

    # print(j["FoundRows"])
    # print(j["LastUniqID"])
    dt =None
    for n in j:
        if(n != "Data") :print(n,'*****',j[n],end=';')
    print()
    dt = j["Data"]
    data['UniqID']=j["LastUniqID"]
    # print(j["Data"])


    # print('find task_id',dt)


    c=0
    list = dt.split('<task_id>')
    s= str(j["LastUniqID"])+","+ str(j["FoundRows"])+",\t"
    s+=data['FromDate'] +"," + data['ToDate']+"\n"
    # f.write(s+"\n")
    for nl in range(1,len(list)):
        all +=1
        l = list[nl]
        k = l.split('</')
        dic = {}
        c += 1
        dic['task_id']=k[0]
        for n in range(1,len(k)):
            s = k[n][k[n].find('<')+1:]
            s=s.replace("![CDATA[","")
            s=s.replace("]]","")
            s=s.replace("<","")
            s = s.split('>')
            dic[s[0]]=s[1]
        dic["client_name"] = dic["client_name"].replace('\n','')
        s = str(c)+"]["
        s+=dic["task_id"]+"],["
        s+=dic["client_id"]+"],["
        s+=dic["start_date"]+"],["
        s+=dic["due_date"]+"],["
        s+=dic["create_date"]+"],["
        s+=dic["update_date"]+"]<<"
        safe = datetime.now()
        if task_update(dic) < 0:
            log("Error db"+str(dic))
            exit(1)
        safe = None
        # print(s)
        # log(str(StartDate)+"="+str(dic))

    # break
    print("=====",all)
print("all readed=====",all)
log(" end , readed "+str(all))
