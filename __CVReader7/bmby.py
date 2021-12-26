import requests
import json

def send_post():
    url = 'http://www.bmby.com/webservices/srv/clients.php?wsdl'
    ProjectID = '8056'
    Password = '051218'
    # Password = 'zxc2810'
    data = {}
    data['ProjectID'] = ProjectID
    data['Password'] = Password
    # data ['Login'] = 'rtgroup'
    data ['UniqID'] = 1
    # data ['ClientID'] = 0
    data ['FromDate'] = '2018-11-01'
    data ['ToDate'] = '2019-01-02'
    data ['Dynamic'] = 1
    ret = 0

    headers = {'Content-type': 'application/json', 'Content-Type': 'text/plain'}
    # ret = requests.post( 'https://www.bmby.com/WebServices/srv/v3/?wsdl' ,data=  data,headers=headers)
    ret = requests.post( 'https://www.bmby.com/WebServices/srv/v3/?wsdl' ,json=json.dumps(data),headers=headers)
    print("text")
    print(ret.encoding)
    print("return value \n",ret.text,"\n reason\n",ret.reason)
    print('ret json ',ret.raise_for_status())
    print( 'headers ::',ret.headers)
    # print(ret.data)
    if ret.raise_for_status():
        print(ret.json())
    print( ret.raw.read(100))

    return ret
send_post()
