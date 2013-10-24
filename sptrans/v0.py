"""Module for the v0 version of the SPTrans API.

The first thing you have to do, in order to use it, is to instantiate a client and authenticate to the API:
>>> client = Client()
>>> client.authenticate('this is my token')
Then you can use the other methods to grab data from the API.
"""

from collections import namedtuple
import json
try:
    from urllib import urlencode
except ImportError:  # pragma: no cover
    from urllib.parse import urlencode

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
STOP_FIELDS = [
    'code',
    'name',
    'address',
    'latitude',
    'longitude',
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


class Stop(namedtuple('Stop', STOP_FIELDS)):

    @classmethod
    def from_dict(cls, stop_dict):
        return cls(
            code=stop_dict['CodigoParada'],
            name=stop_dict['Nome'],
            address=stop_dict['Endereco'],
            latitude=stop_dict['Latitude'],
            longitude=stop_dict['Longitude'],
        )


class Client(object):
    cookies = None

    def build_url(self, endpoint, **kwargs):
        query_string = urlencode(kwargs)
        return '{}/{}?{}'.format(BASE_URL, endpoint, query_string)

    def get_content(self, endpoint, **kwargs):
        url = self.build_url(endpoint, **kwargs)
        response = requests.get(url, cookies=self.cookies)
        return response.content.decode('latin1')

    def get_json(self, endpoint, **kwargs):
        content = self.get_content(endpoint, **kwargs)
        result_list = json.loads(content)
        return result_list

    def authenticate(self, token):
        url = self.build_url('Login/Autenticar', token=token)
        result = requests.post(url)
        self.cookies = result.cookies

    def search_lines(self, keywords):
        result_list = self.get_json('Linha/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Line.from_dict(result_dict)

    def search_stops(self, keywords):
        result_list = self.get_json('Parada/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)
