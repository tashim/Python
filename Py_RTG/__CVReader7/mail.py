#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.4.
#
import imaplib
import email
import email.header
import base64
import binascii
from datetime import datetime

# import mailparser
# import string
# import os
# import pymysql
# import sys
# import datetime
# from dateutil import parser
# import getpass

#EMAIL_ACCOUNT = "Doron.rted"
EMAIL_ACCOUNT = "lidimrtg@gmail.com"
EMAIL_PASSWORD = '0503309318rt'
# EMAIL_ACCOUNT = "Doron.rted@gmail.com"
# EMAIL_PASSWORD = 'Yokasta!'
EMAIL_FOLDER = "INBOX"
import dbMan

import quopri
def html_parse(Payload):
    # print ('in parse_payload')
    try:
        base64.b64decode(Payload)
    except binascii.Error:
        print("not correct base64")
        return
    try:
        msg_text = base64.b64decode(Payload)#.decode('UTF-8')
        print(msg_text,'decded')
    except UnicodeDecodeError:
        print('UTF-8 is in incorrect format')
        # return
    dic={"telefon":'',"city":'',"email":'','"name":'','"domain":''}
    print(type(msg_text))
    msg_text = str(Payload, 'windows-1255')
    print(msg_text)
    lines = msg_text.split('\n')
    for line in lines:
        line = line.replace('*','')
        line = line.replace('\r','')
        line = line.replace('\t','')

def parse_payload(Payload):
    # print ('in parse_payload')
    try:
        base64.b64decode(Payload)
    except binascii.Error:
        print("not correct base64")
        return
    try:
        msg_text = base64.b64decode(Payload).decode('UTF-8')
    except UnicodeDecodeError:
        print('UTF-8 is in incorrect format')
        return
    dic={"telefon":'',"city":'',"email":'','"name":'','"domain":''}
    lines = msg_text.split('\n')
    for line in lines:
        line = line.replace('*','')
        line = line.replace('\r','')
        line = line.replace('\t','')
        nl=line.split(':')
        if not len(nl)==2 : continue
        nl[1]=str(nl[1]).replace('קורס','')
        nl[1]=str(nl[1]).strip()
        if line.find("טל") != -1:
            tel = nl[1].replace('-','')
            dic.update({"telefon":tel})
        if line.find('עיר') != -1:
            dic.update({"city":nl[1]})
        if line.find('מייל') != -1:
            dic.update({"email":nl[1].replace(' ','')})
        if line.find('פרט') != -1:
            dic = {"telefon": '',"city":'',"email": '', '"name":'','"domain": ''}
            dic.update({"name":nl[1]})
        if line.find('משפחה') != -1:
            dic.update({"fname":nl[1]})
        if line.find('מסלול') != -1:
            # dom = nl[1].replace('קורס','')
            dic.update({"domain":nl[1]})
            # new_lead_list.append(dic)
            dbMan.set(dic)

    # print("===>", dic)

    # print ('end of parse')

def parse_payload_yoram(Payload):
    # print ('in parse_payload')
    try:
        base64.b64decode(Payload)
    except binascii.Error:
        print("not correct base64")
        return
    try:
        msg_text = base64.b64decode(Payload).decode('UTF-8')
    except UnicodeDecodeError:
        print('UTF-8 is in incorrect format')
        return
    dic = {"telefon": '', "city": '', "email": '', "fname": '', '"name":'','"domain": '','toar':'\n'}
    lines = msg_text.split('\n')
    for line in lines:
        line = line.replace('*','')
        line = line.replace('\r','')
        line = line.replace('\t','')
        nl=line.split(':')
        if not len(nl)==2 :
            continue
        print(nl)
        nl[1]=str(nl[1]).replace('קורס','')
        nl[1]=str(nl[1]).strip()
        if line.find("טל") != -1:
            tel = nl[1].replace('-','')
            dic.update({"telefon":tel})
        elif line.find('עיר') != -1:
            dic.update({"city":nl[1]})
        elif line.find('דוא') != -1:
            dic.update({"email":nl[1].replace(' ','')})
        elif line.find('שם') != -1:
            name= nl[1].split(' ')
            dic.update({"name":name[0]})
            dic.update({"fname":name[1]})
        elif line.find('קורס') != -1:
            # dom = nl[1].replace('קורס','')
            dic.update({"domain":nl[1]})
            # new_lead_list.append(dic)
        elif line.find('תואר') != -1 or line.find('תחום') != -1 or line.find('קטגוריה') != -1:
            dic.update({'toar':dic['toar']+line+'\n'})
    dbMan.set(dic)

    # print("===>", dic)

    # print ('end of parse')


def process_mailbox(M):

    print('in Process_mailbox')
    rv, data = M.search(None, "UNSEEN")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        print(num)
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        print('mesg from::',msg['From'])
        if (msg['From'].find('TELESERVICE') == -1):
             continue
        else:
            from_m='TELESERVICE'
        # continue
        # hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        dt = str(msg['Date']).split(" ");
        dt = dt[1]+' '+dt[2]+' ' + dt[3] + ' ' + dt[4]
        # date =  datetime.strptime(dt ,'%d %b  %Y %H:%M:%S')
        # date = parser.parser(msg['Date'])
        print("\n",dt)
        # dt = datetime.today() - timedelta(days=4)
        #
        # if dt > date :
        #     M.store(num, '+FLAGS', '\\Deleted')
        #     print("\n", date.date(), date.time(), dt)
        #     print("delete")
        #     continue
        payloads = email.message.EmailMessage.get_payload(msg)
        if (msg.is_multipart()==False):
            print('not multypart')
            cur = msg.get_payload(decode=True)
            type = msg.get_content_type()
            print(cur)
            if (type == 'text/plain'):
                if from_m == 'info':
                    print('pasr info')
                    parse_payload(cur)
                elif from_m == 'yoram':
                    print('parse yoram')
                    parse_payload_yoram(cur)
            else:
                print(cur)
                html_parse(cur)
        else:
            # print('multypart')
            for payload in payloads :

                cur = email.message.EmailMessage.get_payload(payload)
                type = payload.get_content_type()
                if (type == 'text/plain'):
                    if from_m == 'info':
                        parse_payload(cur)
                    elif from_m == 'yoram':
                        parse_payload_yoram(cur)
        break
    M.expunge()

def main():
    try:
        M = imaplib.IMAP4_SSL("imap.gmail.com",993)
    except imaplib.IMAP4.ssl.error:
        print(imaplib.IMAP4.ssl.error)
        print("imaplib FAILED!!! ")
        return (1)

    try:
        rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        print(imaplib.IMAP4.error)
        print ("LOGIN FAILED!!! ")
        return (1)
    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)

    M.logout()


dbMan.connnect()
print('start',datetime.now())
main()
print('end',datetime.now())
dbMan.con_close()
