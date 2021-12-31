#!/usr/bin/env python3
import json
import os
import sys
import random

import requests
import skpy


class SkypeSearch:
    def __init__(self, token):
        self.skype_token = token
        self.session = requests.session()
        self.session.headers.update({
            "X-Skypetoken": self.skype_token,
            "X-ECS-ETag": "Fzn/9gnnfHwbTYyoLcWa1FhbSVkgRg28SzNJqolgQHg=",
            "X-Skype-Client": "1419/8.26.0.70",
            "X-SkypeGraphServiceSettings": '{"experiment":"MinimumFriendsForAnnotationsEnabled","geoProximity":"disabled","minimumFriendsForAnnotationsEnabled":"true","minimumFriendsForAnnotations":2,"demotionScoreEnabled":"true"}',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0',
        })

    def search(self, search_query):
        params = {
            "searchString": search_query,
            "requestId": random.randint(1e13, 9e13)
        }

        search_response = self.session.get("https://skypegraph.skype.com/v2.0/search", params = params)
        if search_response.status_code == 200:
            json_response = search_response.json()
            relevant_data = json_response["results"]
            output = []

            for info in relevant_data:
                output.append(info["nodeProfileData"])

            return output

        return []


def extract():
    if len(sys.argv) == 1:
        term = input('Input phone (or something other) for Skype contact search: ')
    else:
        term = sys.argv[1]

    sk = None
    token_file = './tokens.txt'

    if os.path.exists(token_file):
        sk = skpy.Skype(connect=False)
        sk.conn.tokenFile = token_file
        sk.conn.readToken()

    if not sk or not sk.conn.tokens:
        login = os.getenv('SKYPE_LOGIN') or input('Login: ')
        passw = os.getenv('SKYPE_PASS') or input('Password: ')
        sk = skpy.Skype(login, passw, token_file)

    search = SkypeSearch(token=sk.conn.tokens['skype'])
    res = search.search(search_query=term)

    print(json.dumps(res, indent=4))


if __name__ == '__main__':
    extract()