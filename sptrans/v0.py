"""Module for the v0 version of the SPTrans API.

The first thing you have to do, in order to use it, is to instantiate a client and authenticate to the API:
>>> client = Client()
>>> client.authenticate('this is my token')
Then you can use the other methods to grab data from the API.
"""

from collections import namedtuple
from datetime import date, datetime, time
import json
try:
    from urllib import urlencode
except ImportError:  # pragma: no cover
    from urllib.parse import urlencode

import requests


BASE_URL = 'http://api.olhovivo.sptrans.com.br/v0'


LINE_MAPPING = {
    'code': 'CodigoLinha',
    'circular': 'Circular',
    'sign': 'Letreiro',
    'direction': 'Sentido',
    'type': 'Tipo',
    'main_to_sec': 'DenominacaoTPTS',
    'sec_to_main': 'DenominacaoTSTP',
    'info': 'Informacoes',
}
STOP_MAPPING = {
    'code': 'CodigoParada',
    'name': 'Nome',
    'address': 'Endereco',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
}
LANE_MAPPING = {
    'code': 'CodCorredor',
    'cot': 'CodCot',
    'name': 'Nome',
}
VEHICLE_MAPPING = {
    'plate': 'p',
    'a': 'a',
    'latitude': 'py',
    'longitude': 'px',
}


class MappedTuple(object):
    MAPPING = {}

    @classmethod
    def from_dict(cls, result_dict):
        kwargs = {key: result_dict[value] for key, value in cls.MAPPING.items()}
        return cls(**kwargs)


def build_tuple_class(name, mapping):
    base_classes = (namedtuple(name, mapping.keys()), MappedTuple)
    return type(name, base_classes, {'MAPPING': mapping})


Line = build_tuple_class('Line', LINE_MAPPING)
Stop = build_tuple_class('Stop', STOP_MAPPING)
Lane = build_tuple_class('Lane', LANE_MAPPING)
Vehicle = build_tuple_class('Vehicle', VEHICLE_MAPPING)


POSITION_FIELDS = [
    'time',
    'vehicles',
]


class Positions(namedtuple('Positions', POSITION_FIELDS)):

    @classmethod
    def from_dict(cls, result_dict):
        internal_dicts = result_dict['vs']
        tuples = [Vehicle.from_dict(internal_dict) for internal_dict in internal_dicts]

        hour_parts = result_dict['hr'].split(':')
        hour, minute = [int(part) for part in hour_parts]
        today = date.today()
        time_ = time(hour=hour, minute=minute)
        date_and_time = datetime.combine(today, time_)

        return cls(
            time=date_and_time,
            vehicles=tuples,
        )


class Client(object):
    cookies = None

    def _build_url(self, endpoint, **kwargs):
        query_string = urlencode(kwargs)
        return '{}/{}?{}'.format(BASE_URL, endpoint, query_string)

    def _get_content(self, endpoint, **kwargs):
        url = self._build_url(endpoint, **kwargs)
        response = requests.get(url, cookies=self.cookies)
        return response.content.decode('latin1')

    def _get_json(self, endpoint, **kwargs):
        content = self._get_content(endpoint, **kwargs)
        result_list = json.loads(content)
        return result_list

    def authenticate(self, token):
        url = self._build_url('Login/Autenticar', token=token)
        result = requests.post(url)
        self.cookies = result.cookies

    def search_lines(self, keywords):
        result_list = self._get_json('Linha/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Line.from_dict(result_dict)

    def search_stops(self, keywords):
        result_list = self._get_json('Parada/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def search_stops_by_line(self, code):
        result_list = self._get_json('Parada/BuscarParadasPorLinha', codigoLinha=code)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def search_stops_by_lane(self, code):
        result_list = self._get_json('Parada/BuscarParadasPorCorredor', codigoCorredor=code)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def list_lanes(self):
        result_list = self._get_json('Corredor')
        for result_dict in result_list:
            yield Lane.from_dict(result_dict)

    def get_positions(self, code):
        result_dict = self._get_json('Posicao', codigoLinha=code)
        return Positions.from_dict(result_dict)
