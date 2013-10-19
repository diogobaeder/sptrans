"""Module for the v0 version of the SPTrans API.

The first thing you have to do, in order to use it, is to instantiate a client and authenticate to the API:
>>> client = Client()
>>> client.authenticate('this is my token')
Then you can use the other methods to grab data from the API.
"""

from collections import namedtuple
import json

import requests


BASE_URL = 'http://api.olhovivo.sptrans.com.br/v0'


LINE_FIELDS = [
    'code',
    'circular',
    'sign',
    'direction',
    'type',
    'main_to_sec',
    'sec_to_main',
    'info',
]


class Line(namedtuple('Line', LINE_FIELDS)):

    @classmethod
    def from_dict(cls, line_dict):
        return cls(
            code=line_dict['CodigoLinha'],
            circular=line_dict['Circular'],
            sign=line_dict['Letreiro'],
            direction=line_dict['Sentido'],
            type=line_dict['Tipo'],
            main_to_sec=line_dict['DenominacaoTPTS'],
            sec_to_main=line_dict['DenominacaoTSTP'],
            info=line_dict['Informacoes'],
        )


class Client(object):
    cookies = None

    def authenticate(self, token):
        result = requests.post('{}/Login/Autenticar?token={}'.format(BASE_URL, token))
        self.cookies = result.cookies

    def search_lines(self, keywords):
        response = requests.get()
        response_list = json.loads(response.content)

        for line_dict in response_list:
            yield Line.from_dict(line_dict)
