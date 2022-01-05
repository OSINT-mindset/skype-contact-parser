import asyncio
import os
import random
from typing import List, Any

from aiohttp import TCPConnector, ClientSession
from bs4 import BeautifulSoup as bs
import skpy

from .executor import AsyncioProgressbarQueueExecutor


class InputData:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class OutputData:
    def __init__(self, values, error):
        self.error = error
        self.skype_id = values.get('skypeId')
        self.avatar_url = f'https://avatar.skype.com/v1/avatars/{self.skype_id}/public'
        self.handle = values.get('skypeHandle')
        self.name = values.get('name')
        self.country_code = values.get('countryCode')
        self.city = values.get('city')
        self.state = values.get('state')
        self.contact_type = values.get('contactType')

    @property
    def fields(self):
        fields = list(self.__dict__.keys())
        fields.remove('error')

        return fields

    def __str__(self):
        error = ''
        if self.error:
            error = f' (error: {str(self.error)}'

        result = ''
        result += f'Skype ID: {str(self.skype_id)}\n'
        if self.skype_id != self.handle:
            result += f'Username: {str(self.handle)}\n'

        for field in ('name', 'country_code', 'city', 'state', 'avatar_url'):
            field_pretty_name = field.title().replace('_', ' ')
            value = self.__dict__.get(field)
            if value:
                result += f'{field_pretty_name}: {str(value)}\n'

        result += f'{error}'

        return result


class OutputDataList:
    def __init__(self, input_data: InputData, results: List[OutputData]):
        self.input_data = input_data
        self.results = results

    def __repr__(self):
        return f'Target {self.input_data}:\n' + '--------\n'.join(map(str, self.results))


class Processor:
    def __init__(self):
        connector = TCPConnector(ssl=False)
        self.session = ClientSession(
            connector=connector, trust_env=True
        )

        sk = None
        token_file = './tokens.txt'

        try:
            if os.path.exists(token_file):
                sk = skpy.Skype(connect=False)
                sk.conn.tokenFile = token_file
                sk.conn.readToken()
        except skpy.core.SkypeAuthException as e:
            print(e)

        if not sk or not sk.conn.tokens:
            login = os.getenv('SKYPE_LOGIN') or input('Login: ')
            passw = os.getenv('SKYPE_PASS') or input('Password: ')
            sk = skpy.Skype(login, passw, token_file)

        self.skype_token = sk.conn.tokens['skype']

    async def close(self):
        await self.session.close()

    async def request(self, input_data: InputData) -> OutputDataList:
        contacts = []
        error = None

        headers = {
            "X-Skypetoken": self.skype_token,
            "X-ECS-ETag": "Fzn/9gnnfHwbTYyoLcWa1FhbSVkgRg28SzNJqolgQHg=",
            "X-Skype-Client": "1419/8.26.0.70",
            "X-SkypeGraphServiceSettings": '{"experiment":"MinimumFriendsForAnnotationsEnabled","geoProximity":"disabled","minimumFriendsForAnnotationsEnabled":"true","minimumFriendsForAnnotations":2,"demotionScoreEnabled":"true"}',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0',
        }

        try:
            term = input_data.value
            params = {
                "searchString": term,
                "requestId": random.randint(1e13, 9e13)
            }

            search_response = await self.session.get("https://skypegraph.skype.com/v2.0/search", headers=headers, params=params)
            if search_response.status == 200:
                json_response = await search_response.json()
                relevant_data = json_response["results"]

                for info in relevant_data:
                    contacts.append(OutputData(info["nodeProfileData"], None))

        except Exception as e:
            error = e

        results = OutputDataList(input_data, contacts)

        return results


    async def process(self, input_data: List[InputData]) -> List[OutputDataList]:
        tasks = [
            (
                self.request, # func
                [i],          # args
                {}            # kwargs
            )
            for i in input_data
        ]

        results = await AsyncioProgressbarQueueExecutor().run(tasks)

        return results
