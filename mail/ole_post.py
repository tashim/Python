#!/usr/bin/env python3
# send post to cloud
# sed LID data
# #

import requests
import json
from dbManFace import get_Indiv


# from dbManFace import *

def send_to_oleg(entryID,sProdact,sSource):
    if not entryID: return
    if type(entryID) == type((1,)): entryID = entryID[0]
    if type(entryID) == type([]): id = entryID[0]
    print('send to Oleg')
    data = get_Indiv(entryID)
    # print(data)
    branch = 0
    if   data['location'] < 100: branch = 100 # rishon
    elif data['location'] == 100: branch = 200 # tel-aviv
    elif data['location'] == 200: branch = 300 # heifa

    dic_data={
        'EntryDate': data['NewEntryDate'],
        'FirstName': data['FirstName'],
        'LastName': data['LastName'],
        'personID': data['personID'],
        'Phone1': data['Phone1'],
        'Phone2':  data['Phone2'],
        'Email': data['Email'],
        'Address': data['Address'],
        'branch': branch,
        'product': sProdact, #v string
        'source': sSource,# INT  SEO SNL(fase) DEF
        'CV': data['CV'],
        'file_path': data['file_path'],
        'entryID': data['entryID'],
        'Activities': data['Activities'],
        'ContactType': data['ContactType'],
        'b_entryID': data['b_entryID']
     }
    individual =     { 'individual':dic_data}


    individual = json.dumps(individual)
    # data = json.dumps(data)
    print(individual)
    heder = {"Content-Type": "application/json"}
    # ret = requests.post('http://192.117.146.228:3000/api/person/newfromscript',headers=heder ,data=individual)
    ret = requests.post('http://45.83.43.173:3000/api/person/newfromscript',headers=heder ,data=individual)

    print("return value from Oleg :\n ", data['location'],dic_data['branch'],'\n\n',ret.text, ret.reason)

