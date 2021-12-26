import urllib.request
from pathlib import Path

import requests
import json
import webbrowser
from Keywords import credentials


class UnickoApi:
    BASE_URL = 'https://api.unicko.com/v1'
    HEADERS = {'Content-Type': 'application/json'}
    HTTP_CODE_SUCCESS = 200
    HTTP_CODE_CREATED = 201
    HTTP_CODE_NO_CONTENT = 204
    http_status_codes = {
        'get': HTTP_CODE_SUCCESS,
        'create': HTTP_CODE_CREATED,
        'delete': HTTP_CODE_NO_CONTENT,
        'post': HTTP_CODE_SUCCESS
    }

    def single_request_get(self, url, action='get', *args, **kwargs) -> dict:
        # print(f'requesting {url}')         # Viewing all requested URL's
        response = getattr(requests, action)(url, headers=self.HEADERS, auth=credentials, *args, **kwargs)
        # if response.status_code != self.http_status_codes[action]:
        #     print(response.status_code)
        #     print(response.content)
            # raise RuntimeError(f'Run Time Error code: {response.status_code}')
        if response.status_code == self.HTTP_CODE_NO_CONTENT:
            return {}
        response = response.content.decode('utf-8')
        if len(response) == 0:
            return {}
        return json.loads(response)

    def request(self, url, *args, **kwargs):
        url = self.BASE_URL + '/' + url
        # print(url)
        response_items = []
        while True:
            response = self.single_request_get(url, *args, **kwargs)
            if 'items' not in response:
                return [response]
            response_items += response['items']
            # Is there a next page available?
            if 'paging' in response and 'next' in response['paging']:
                url = response['paging']['next']
            else:
                break
        return response_items

    def list_all_meetings(self, order="asc"):
        """
        :arg order asc (Ascending) or desc (Descending)
        """
        return self.request('meetings', params={"order": order,"page_size":"50"})

    def list_all_meetings_minimal(self, order="asc"):
        """
        :arg order asc (Ascending) or desc (Descending)
        """
        data = self.request('meetings', params={"order": order})
        total = 0
        for i in data:
            total += 1
            print("Meeting Name:", i['name'], ', ', "Meeting ID:", i['id'])
        print("Total Meetings:", total)

        return data

    def list_all_recordings(self, order="asc"):
        """
        :arg order asc (Ascending) or desc (Descending)
        """
        return self.request('recordings', params={"order": order})

    def get_specific_recording(self, id):
        """
        :arg id recording ID
        """
        return self.request('recordings/{}'.format(id))[0]

    def list_all_recordings_minimal(self, order="asc"):
        """
        :arg order asc (Ascending) or desc (Descending)
        """
        data = self.request('recordings', params={"order": order})
        total = 0
        for i in data:
            total += 1
            print("Meeting ID:", i['meeting'], "Recording ID:", i['id'])
        print("Total Recording:", total)

        return data

    def get_specific_user(self, id):
        """
        :arg id user ID
        """
        return self.request('users/{}'.format(id))[0]

    def list_all_users(self, order="asc"):
        return self.request('users', params={"order": order})

    def list_all_users_minimal(self, order="asc"):
        data = self.request('users', params={"order": order})
        total = 0
        for i in data:
            total += 1
            print("User Name: ", i['last_name'], ', ', "First Name: ", i['first_name'], ', ', "User ID:", i['id'])
        print("Total Users:", total)

        return data

    def get_specific_meeting(self, id):
        """
        :arg id meeting ID
        """
        return self.request('meetings/{}'.format(id))[0]

    def get_specific_meeting_name(self, id):
        return self.request('meetings/{}'.format(id))[0]

    def delete_recording(self, id):
        """
        :arg id recording ID
        """
        return self.request('recordings/{}'.format(id), action="delete")[0]

    def download_recording(self, recording, downloads_folder):
        """
        :arg recording recording ID
        """
        recording_url = recording['download_url']
        # print(recording_url)
        # os.system(f'curl {recording_url}') # FORBIDDEN 403
        # webbrowser.get('google-chrome').open(recording_url) # Original
        # self.B.open(recording_url) # Original
        print("Downloading recording", recording["id"], "...")
        Path(downloads_folder).mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(recording_url, f"{downloads_folder}" + "/" + "recording_" + recording["id"] + ".mp4")

    def create_meeting(self, name, id):
        """
            :arg id Meeting ID - [ 1 .. 32 ] characters
            :arg name Meeting Name - [ 1 .. 150 ] characters
            """
        id = str(id)
        self.request("meetings", action="post", params={"name": name, "id": id})

    def delete_meeting(self, id):
        """
         :arg id meeting ID
         """
        id = str(id)
        return self.request('meetings/{}'.format(id), action="delete")[0]

    def url_meeting(self,meeting_id='336723022',id=1555192):
        id = str(id)
        # https://api.unicko.com/v1/meetings/{meeting_id}/host_url
        url = f"meetings/{meeting_id}/host_url"
        self.request(url, action="post", data=json.dumps({ "id": id}))

vUnicko = UnickoApi()
if __name__ == "__main__":
    # for i in UnickoApi().list_all_users() :
    #     print(i)
    # list_meet = vUnicko.list_all_meetings()
    list_meet = vUnicko.list_all_meetings_minimal()
    for f in list_meet:
        print(f)
    print("list_meet",len(list_meet))
    # print(UnickoApi().get_specific_meeting(431851634))
    # print(UnickoApi().get_specific_meeting(430846777))