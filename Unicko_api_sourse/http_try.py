# import requests module
import webbrowser

from Keywords import credentials
import json
import requests

# Making a get request
HEADERS = {'Content-Type': 'application/json'}

def users():
    url = 'https://api.unicko.com/v1/users'
    response = requests.get(url,headers=HEADERS, auth=credentials)
    d1=json.loads(response.text)
    return d1['items']

def meetings():
    url = 'https://api.unicko.com/v1/meetings'
    response = requests.get(url,headers=HEADERS, auth=credentials)
    d1=json.loads(response.text)
    return d1['items']

def url_meeting(meeting_id,id):
    id = str(id)
    # https://api.unicko.com/v1/meetings/{meeting_id}/host_url
    url = f"https://api.unicko.com/v1/meetings/{meeting_id}/host_url"
    response = requests.post(url,headers=HEADERS, auth=credentials,  data=json.dumps({ "id": id}))
    d1=json.loads(response.text)
    return d1

def url_s_meeting(meeting_id,id):
    id = str(id)
    # https://api.unicko.com/v1/meetings/{meeting_id}/host_url
    url = f"https://api.unicko.com/v1/meetings/{meeting_id}/attendee_url"
    response = requests.post(url,headers=HEADERS,
             auth=credentials,
             data=json.dumps({
                 "ext_id": id,
                 "first_name": "fname",
                 "last_name": "last_name"
             }).encode())
    d1=json.loads(response.text)
    return d1

if __name__=="__main__":
    usr = users()
    for i,jj in enumerate( usr ):
        print(f"{i}\t{jj['id']}\t,\t{jj['role']}\t,"
              f"\t{jj['first_name']} {jj['last_name']}")
    while True:
        try:
            i = int(input('user >> '))
            if(i<len(usr)):               break
        except:    pass
    usr = usr[i]
    meet = meetings()
    for i,jj in enumerate( meet ):
        print(f"{i}\t{jj['id']}\t{jj['name']}")
    while True:
        try:
            i = int(input('meeting >> '))
            if(i<len(meet)):               break
        except:    pass
    meet = meet[i]
    # print(f"{i}\t{meet['id']}\t{meet['name']}\t{meet['ext_id']}")
    # ourl = url_s_meeting(meet['id'],meet['ext_id'])['url']
    # webbrowser.open(ourl)
    ourl = url_meeting(meet['id'],usr['id'])['url']
    webbrowser.open(ourl)
