from database import *
from unicko_api import *

# print(vUnicko.get_specific_meeting(454964172))
guery = """SELECT url_conference,code FROM coursecycle 
    where url_conference = {}
    ; 
    
    """
ret = vUnicko.list_all_meetings()
# ret = RTG_DB.run_query(guery)
n=0
for q in ret:
    # print(q['id'])
    dbret = RTG_DB.run_query(guery.format(q['id']))
    if len(dbret)>0:
        pass
        # print(dbret[0])
    else:
        print('empty',q['id'])
        vUnicko.delete_meeting(q['id'])
        n +=1
    # get = vUnicko.list_all_meetings()
    # get = vUnicko.get_specific_meeting(q[0])
print(len(ret))
print(n)
