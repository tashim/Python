import datetime
import os
import sys
from datetime import date, timedelta, datetime

from future.backports.datetime import timedelta

# from DB import *
# from Soap1 import *
import re

d = datetime.now()
# fileName = os.path.basename(__file__).split('.')[0]+d.strftime( "%d_%m_%y")+".log"
fn = sys.argv[0].split("/")[-1]
fn = sys.argv[0].split("\\")[-1]
fileName = fn.split('.')[0]+d.strftime( "_%d_%m_%y")+".log"
print(fileName)
def log(text):
    try:
        file = open(fileName,'a+')
    except:
        file = open(fileName,'w+')
    # print( file.read() )
    file.write(str(datetime.now())+" | "+text+"\n")
    file.close()


if __name__ == '__main__':
    StartDate = "30/10/11"

    Date = datetime.now()
    print(Date.strftime("%Y-%m-%d %H:%M"))

    print("hhh")
    print(os.path.basename(__file__))
    input("text")
    EndDate = Date + timedelta(days=10)
    print(EndDate.strftime("%Y-%m-%d"))
    # media = "Intel"
    # status = 'def'
    # print(get_company_id(media))
    # print(get_media_ID_ST(media))
    # print(get_status_id(status))
    # n,c = find_in_sm("82450")
    # print(n)
    # print(c)
    # for i in c:
    #     print(n,i,">>",c)
        # for y in i:
        #     print(y,i[y],":",y,type(i[y]))
    #print(type(i))
    # Updete_Double([1012318,1017956])
    # Updete_Sm_for_Double()
    # dbsm.close()
