from datetime import datetime, date, timedelta

from DbReadTest import *
from unicko_api import *

#######################################################
#
# days from now to remove meeting
days_from_now = 33
#
#######################################################


meet_deleted = 0      # total meetings checked for delete
clean_cource = 0  # total meetings deleted

ret = vUnicko.list_all_meetings()

for q in ret:
    # print(q['id'])
    if not q["ext_id"]:  # those with none idx_id dont tuch
        continue
    if len(q["ext_id"])<2:
        continue

    may_be_del = True
    dbret = RTG_DB.get_cource_by_unicoID(q['id'])
    if dbret:
        for cource in dbret:
            if datetime.now().date() - cource[2] < timedelta(days_from_now):
                may_be_del = False
    if may_be_del:
        # TODO delete meeting
        print('rm unico', q['id'])
        # vUnicko.delete_meeting(q['id'])
        meet_deleted +=1
        if dbret:
            for cource in dbret:
                print('rm co',dbret[0],cource[2],datetime.now().date() - cource[2])
                # TODO rem mettingId from COUrse
                clean_cource +=1
                # RTG_DB.rm_unicoID_from_cource(cource[1])

print("total of unicko meeting at start = ", len(ret))
print('delete m',meet_deleted)
print('delete c',clean_cource)
print('meet without c',meet_deleted - clean_cource)
print('meets ',len(ret) - meet_deleted )