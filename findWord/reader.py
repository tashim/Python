
# Imports
import os
import shutil
import sys
import datetime
import pymysql
import MySQLdb


# from FileManager import makeItRain
# from DbMan import setDB,connnect,con_close
from Scan import *
from DatabaseManager import saveData
from FManager import makeItRain

# import post
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
def scanFiles(service,domain=None,word=""):
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
    save_path = dir_path+'CVfind/'+ 'passed/'
    save_path_bad = dir_path+'CVfind/'+ 'not_passed/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'+service+domain_path +'/'
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
                # try:
                #     shutil.move(file_path + fileName, save_path_bad + fileName)
                #     print("file", fileName, " moved to trash")
                # except WindowsError as e:
                #     print(e)
                continue
            """
        Scan info from data
"""

            person = scanPhone(data,word)
            if person == None : continue
            print('finded data :', person)
            p_domain = domain
            # copyfile(file_path + fileName, save_path+fileName)
            print("=========================================================================================================================================")
            print(file_path + fileName, save_path+'/'+word+'/'+fileName)
            # copyfile(file_path + fileName, save_path+'/'+word+'/'+fileName)
            file = open(save_path+"/text3.csv","a+")
            for ft in person:
                if ft != "word":
                    if person[ft] == "" :
                        file.write('None,')
                    else:
                        file.write(person[ft]+',')
            file.write("\n")
            file.close()
            print(person["word"])

    print('from ',service,'[',domain,']',getCounter())
    # os.system("pause")


def main_fun(service,word=""):
    global \
        temp_path, \
        dir_path, \
        tempFileName
    for fileName in os.listdir(dir_path+'New/'+service+'/'):
        print(dir_path+'New/'+service + '/'+fileName)
        if os.path.isdir(dir_path+'New/' +service+'/'+ fileName):
            scanFiles(service,fileName,word)
    scanFiles(service,None,word)

    # os.system("pause")


if __name__ == '__main__':
    # connnect()
    temp_path = 'c:/antiword/'
    dir_path = 'Z:/SmartCV/'
    tempFileName = 'tempfile'
    main_fun("AllJobs","vhdl")
    main_fun("JobMaster","vhdl")
    main_fun("Runner","vhdl")
    main_fun("Hr","vhdl")
    main_fun("Drushim","vhdl")
    # input("press enter")
    # con_close()