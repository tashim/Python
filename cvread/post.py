
import requests
import json

def send_post(Phone ,CV=' ',ProductTitle='',Fname = 'none' ,Lname='none' ,Address='none' ,Referal='' ,Email='none' ,MediaTitle='none',domain=' '):

    data = {}
    data['AllowedMail'] = '0'
    data['ProjectID'] = '8056'
    data['Password'] = 'zxc2810'
    data ['Phone'] = Phone
    data ['Fname'] = Fname
    data ['Lname'] = Lname
    data ['CV'] = 'file:///'+CV
    data ['ProductTitle'] = ProductTitle
    data ['Comments'] = 'file:///'+ CV+'\n מתניין ב'+domain
    data ['Address'] = Address
    # data ['Referal'] = Referal
    data ['Email'] = Email
    data ['MediaTitle'] = MediaTitle
    ret = 0
    ret = requests.post('http://www.bmby.com/shared/AddClient/index.php' ,data=data)
    print("return value ",ret.text,ret.reason)
    print(data)

    return ret


def send_post2(Phone ,CV='none',ProductTitle='',Fname = 'none' ,Lname='none' ,Address='none' ,Referal='' ,Email='none' ,MediaTitle='none'):
    url = 'http://www.bmby.com/shared/AddClient/index.php'
    ProgectID = '8056'
    Password = 'zxc2810'
    data = {}
    data['AllowedMail'] = '0'
    data['ProjectID'] = '8056'
    data['Password'] = 'zxc2810'
    data ['Phone'] = Phone
    data ['Fname'] = Fname
    data ['Lname'] = Lname
    data ['CV'] = 'file:///'+CV
    data ['ProductTitle'] = ProductTitle
    data ['Comments'] = 'file:///'+ CV
    data ['Address'] = Address
    # data ['Referal'] = Referal
    data ['Email'] = Email
    data ['MediaTitle'] = MediaTitle
    ret = 0
    ret = requests.post('http://www.bmby.com/shared/AddClient/index.php' ,data=data)
    print("return value ",ret.text,ret.reason)
    print(data)

    return ret

def mail_post(Phone ,Comments = '',ProductTitle='',Fname = '' ,Lname='' ,Address='' ,Email='' ,MediaTitle='SEO'):
    url = 'http://www.bmby.com/shared/AddClient/index.php'
    ProgectID = '8056'
    Password = 'zxc2810'
    data = {}
    data['AllowedMail'] = '0'
    data['ProjectID'] = '8056'
    data['Password'] = 'zxc2810'
    data ['Phone'] = Phone
    data ['Fname'] = Fname
    data ['Lname'] = Lname
    data ['ProductTitle'] = ProductTitle
    data ['Comments'] = Comments
    data ['Address'] = Address
    # data ['Referal'] = Referal
    data ['Email'] = Email
    data ['MediaTitle'] = MediaTitle
    ret = 0
    ret = requests.post('http://www.bmby.com/shared/AddClient/index.php' ,data=data)
    print("return value ",ret.text,ret.reason)
    print(data)

    return ret