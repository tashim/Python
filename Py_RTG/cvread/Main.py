
# Imports
import os
import shutil
import sys
import datetime
import pymysql
import MySQLdb


# from FileManager import makeItRain
from Scanners import scanName
from Scanners import scanDate
from Scanners import scanPhone
from Scanners import scanEmail
# from Scanners import scanEducation
from Scanners import setCounter
from Scanners import getCounter
from DatabaseManager import saveData
from FileManager import makeItRain

import post

# if service Drushim , then send post



host2 = '192.168.1.63'
user = 'vadim'
password = '!1+=2018Y'
database = 'smartcv'


gservice = ''

# detects the source of the incoming CV in this upload session
def setService(data):
    global gservice
    try:
        conn = pymysql.connect(host2, user, password, database, charset='utf8')
        cursor = conn.cursor()
        r = cursor.execute('SELECT codeID FROM ContactTypes where type = "'+data+'"')
        gservice = ''.join(map(str, cursor.fetchone()))

    except pymysql.Error as e:
        conn.rollback()
        print ("error db",e)

    if len(gservice) > 0:
        return gservice
    else:
        exit()
        input("Press enter to exit...")

#Main function to call all the methods
def main_fun(service):
    setCounter()

    temp_path = 'c:/antiword/'
    file_path = 'Z:/SmartCV/New/' + service + '/'
    save_path = 'Z:/SmartCV/CVs/' + 'passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/' + service + '/'
    save_path_bad = 'Z:/SmartCV/CVs/' + 'not_passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/' + service + '/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(save_path_bad):
        os.makedirs(save_path_bad)

    for fileName in os.listdir(file_path):
        if os.path.isdir(file_path + fileName):
            continue
        if fileName[-4:] == ".txt" or fileName[-4:] == ".doc" or fileName[-5:] == ".docx" or fileName[-4:] == ".pdf":
            print (fileName)
            try:
                data = makeItRain(fileName, file_path, save_path, temp_path)
                # print data
            except KeyError as e:
                print (e)
                data = ['Bad', 'Bad']
            ext = data[0]
            data = data[1]
            if data == 'Bad':
                print("bad data",fileName)
                try:
                    shutil.move(file_path + fileName, save_path_bad + fileName)
                    print ("file moved to trash")
                except WindowsError as e:
                    print (e)
                continue
            phonephone = 'No Number'
            if data:
                person = []
                person.append(scanName(data))
                person.append(scanDate(data))
                phonephone = scanPhone(data)
                person.append(phonephone)
                person.append(scanEmail(data))
                # text = ' '.join(data)
                text2 = '\n'.join(data)
                location = save_path + phonephone + ext
# #
#TODOO: send post to BMBY
                if phonephone != 'No Number':
                    post.send_post(
                        Phone =  phonephone ,
                        Fname = person[0] ,
                        Lname='' ,
                        CV=location,
                        Address='' ,
                        Referal=service ,
                        Email= person[3],
                        MediaTitle= service)
### write to DB
                    if saveData(person, text2, location, setService(service)) == 1:
# rename file and move
                        try:
                            shutil.move(file_path + fileName, save_path + phonephone + ext)
                        except WindowsError as e:
                            print ("error write pass:",e)
                            # os.remove(save_path + phonephone + ext)
                    else:
                        try:
                            shutil.move(file_path + fileName, save_path_bad  +   fileName)
                        except:
                            print("error write:", save_path_bad +  fileName)
                else:
                    try:
                        shutil.move(file_path + fileName, save_path_bad + fileName)
                    except:
                        print("error write:",save_path_bad + fileName)
            else:
                try:
                    shutil.move(file_path + fileName, save_path_bad + fileName)
                except:
                    print("error write:", save_path_bad + fileName)
        else:
            continue

    print(getCounter())
    # os.system("pause")


if __name__ == '__main__':
    main_fun("AllJobs")
    # main_fun("JobMaster")
    # main_fun("Runner")
    # main_fun("Hr")
    # main_fun("Drushim")
    input("press enter")
