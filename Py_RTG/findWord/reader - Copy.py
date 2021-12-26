
# Imports
import os
import shutil
import sys
import datetime
import pymysql
import MySQLdb


# from FileManager import makeItRain
from Scan import *
from DatabaseManager import saveData
from FManager import makeItRain

import post
from shutil import copyfile
# if service Drushim , then send post


#
# host2 = '192.168.1.63'
# user = 'vadim'
# password = '!1+=2018Y'
# database = 'smartcv'
host2 = '127.0.0.1'
user = 'root'
password = '1234'
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
    file_path = 'c:/AllJobs/'
    save_path = 'c:/AllJobs/' + 'passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'
    save_path_bad = 'c:/AllJobs/' + 'not_passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(save_path_bad):
        os.makedirs(save_path_bad)
    tempFileName='temp'

    for fileName in os.listdir(file_path):
        fileNameOld = fileName
        if os.path.isdir(file_path + fileName):
             continue
        if fileName[-4:][0]=='.':
            if fileName == str(tempFileName) + fileName[-4:]:
                if os.path.isfile(file_path + str(tempFileName) + fileName[-4:]):
                    os.remove(file_path + str(tempFileName) + fileName[-4:])
                continue
            if os.path.isfile(file_path + str(n)+fileName[-4:]):
                os.remove(file_path + str(tempFileName)+fileName[-4:])
            copyfile(file_path + fileName, file_path + str(tempFileName)+fileName[-4:])
            fileName = str(tempFileName)+fileName[-4:]
        if fileName[-5:][0]=='.':
            if fileName == str(tempFileName) + fileName[-5:]:
                if os.path.isfile(file_path + str(tempFileName) + fileName[-5:]):
                    os.remove(file_path + str(tempFileName) + fileName[-5:])
                continue
            if os.path.isfile(file_path + str(tempFileName)+fileName[-5:]):
                os.remove(file_path + str(tempFileName)+fileName[-5:])
            copyfile(file_path + fileName, file_path + str(tempFileName)+fileName[-5:])
            fileName = str(tempFileName) + fileName[-5:]
        print(fileNameOld)

        if fileName[-4:] == ".txt" or fileName[-4:] == ".doc" or fileName[-5:] == ".docx" or fileName[-4:] == ".pdf":
            try:
                 data = makeItRain(fileName, file_path, save_path, temp_path)
                # print data
            except :
                print ('error read file')
                data = ['Bad']
            if data[0] == 'Bad':
                print("bad data",fileName)
                try:
                    # shutil.move(file_path + fileNameOld, save_path_bad + fileNameOld)
                    print ("file moved to trash")
                except WindowsError as e:   print (e)
                continue
            phonephone = 'No Number'
            if len(data)>1:
                person = scanPhone(data[1])
                print(person)
                if person:
                    print("Good data", fileName)
                    try:
                        shutil.move(file_path + fileNameOld, save_path + fileNameOld)
                        print("file moved to pass")
                    except WindowsError as e:
                        print(e)

                else:
                    print("bad data", fileName)
                    try:
                        # shutil.move(file_path + fileNameOld, save_path_bad + fileNameOld)
                        print("file moved to trash")
                    except WindowsError as e:
                        print(e)
                    continue

    print(getCounter())
    # os.system("pause")


if __name__ == '__main__':
    main_fun("AllJobs")
    # main_fun("JobMaster")
    # main_fun("Runner")
    # main_fun("Hr")
    # main_fun("Drushim")
    # input("press enter")
