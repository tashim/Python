
# Imports
import os
import shutil
import sys
import datetime
import pymysql
import MySQLdb


# from FileManager import makeItRain
from DbMan import setDB,connnect,con_close
from Scan import *
from DatabaseManager import saveData
from FManager import makeItRain

import post
from shutil import copyfile
# if service Drushim , then send post
from shutil import copyfile


#
# host2 = '192.168.1.63'
# user = 'vadim'
# password = '!1+=2018Y'
# database = 'smartcv'
host2 = '127.0.0.1'
user = 'root'
password = '1234'
database = 'smartcv'



#Main function to call all the methods
def scanFiles(service,domain=None):
    setCounter()
    global \
        temp_path ,\
        dir_path ,\
        tempFileName

    temp_dir = temp_path+'temp/'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if domain:
        if not domain in ['CYB','DEVOP','FS','QA','RT']: return
        domain_path = '/'+domain+'/'
    else:
        domain_path = '/'

    temp_path = 'c:/antiword/'
    file_path =  dir_path+'New/'+service+domain_path
    # print(file_path)
    save_path = dir_path+'CVs/'+ 'passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'+service+domain_path +'/'
    save_path_bad = dir_path+'CVs/'+ 'not_passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'+service+domain_path +'/'
    if not os.path.exists(save_path):
        # print(save_path)
        # print(save_path_bad)
        os.makedirs(save_path)
    if not os.path.exists(save_path_bad):
        os.makedirs(save_path_bad)

    if os.path.exists(temp_dir + tempFileName+'.doc') :  os.remove(temp_dir + tempFileName+'.doc')
    if os.path.exists(temp_dir + tempFileName+'.txt') :  os.remove(temp_dir + tempFileName+'.txt')
    if os.path.exists(temp_dir + tempFileName+'.docx') :  os.remove(temp_dir + tempFileName+'.docx')
    if os.path.exists(temp_dir + tempFileName+'.pdf') :  os.remove(temp_dir + tempFileName+'.pdf')

    for fileName in os.listdir(file_path):
        if os.path.isdir(file_path + fileName):
            continue
        ext = fileName.split('.')[-1].lower()
        if ext != "txt" \
                and ext != "doc" \
                and ext != "docx" \
                and ext != "pdf":
            continue
        if fileName.replace('.' + ext, '') == tempFileName:
            s = file_path + fileName
            os.remove(file_path + fileName)
            # print('temp file')
            continue
        else:
            fullTempFile = temp_dir + tempFileName + '.' + ext
            copyfile(file_path + fileName, fullTempFile)
            try:
                data = makeItRain(fullTempFile, temp_path, ext)
            except:
                print('error read file')
                data = None
            if not data:
                print("bad data", fileName)
                try:
                    shutil.move(file_path + fileName, save_path_bad + fileName)
                    print("file", fileName, " moved to trash")
                except WindowsError as e:
                    print(e)
                continue
            """
        Scan info from data
"""
            person = scanPhone(data)
            print('finded data :', person)
            p_domain = domain

            if person:
                if not domain:
                    dom = ''
                    p_domain=''
                elif domain == 'QA':
                    dom = 'QA'
                elif domain == 'CYB':
                    dom = 'Cyber course'
                elif domain == 'DEVOP':
                    dom = 'DevOps'
                elif domain == 'FS':
                    dom = 'Full stack'
                elif domain == 'RT':
                    dom = 'Real Time embedded'
                location = save_path + person['Phone'] + '.' + ext
                print('==================================================================')
                post.send_post(
                    Phone=person['Phone'],
                    Fname=person['Name'],
                    Lname='',
                    CV=location,
                    domain=dom,
                    ProductTitle=dom,
                    Email=person['Email'],
                    MediaTitle=service)
                ### write to DB
                dic = {}
                dic["telefon"]=person['Phone']
                dic['domain']=dom
                dic["name"]=person['Name']
                dic["fname"]=''
                dic["email"]=person['Email']
                dic['city']=''
                dic['CV'] = location
                dic['ContactType'] = 101
                dic['service']=service
                dic['TZ']=person['TZ']
                if service=='AllJobs':
                    dic['ContactType']=107
                elif service=='Runner':
                    dic['ContactType'] = 112
                if setDB(dic) == 1:
                    # rename file and move
                    try:
                        shutil.move(file_path + fileName, location)
                        print("file ", fileName, " moved to pass")
                    except WindowsError as e:
                        print(e)
                else:
                    try:
                        shutil.move(file_path + fileName, save_path_bad + fileName)
                    except:
                        print("error write:", save_path_bad + fileName)


            else:
                try:
                    shutil.move(file_path + fileName, save_path_bad + fileName)
                    print("file ", fileName, " moved to trash")
                except WindowsError as e:
                    print(e)
                continue

    print('from ',service,'[',domain,']',getCounter())
    # os.system("pause")


def main_fun(service):
    global \
        temp_path, \
        dir_path, \
        tempFileName
    for fileName in os.listdir(dir_path+'New/'+service+'/'):
        print(dir_path+'New/'+service + '/'+fileName)
        if os.path.isdir(dir_path+'New/' +service+'/'+ fileName):
            scanFiles(service,fileName)
    scanFiles(service)

    # os.system("pause")


if __name__ == '__main__':
    connnect()
    temp_path = 'c:/antiword/'
    dir_path = 'Z:/SmartCV/'
    tempFileName = 'tempfile'
    main_fun("AllJobs")
    # main_fun("JobMaster")
    main_fun("Runner")
    # main_fun("Hr")
    # main_fun("Drushim")
    # input("press enter")
    con_close()