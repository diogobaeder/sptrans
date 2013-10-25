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


class MappedTuple(object):
    MAPPING = {}

    @classmethod
    def from_dict(cls, result_dict):
        kwargs = {}
        for key, value in cls.MAPPING.items():
            if isinstance(value, str):
                kwargs[key] = result_dict[value]
            else:
                kwargs[key] = value.resolve(result_dict)
        return cls(**kwargs)


def build_tuple_class(name, mapping):
    base_classes = (namedtuple(name, mapping.keys()), MappedTuple)
    return type(name, base_classes, {'MAPPING': mapping})


def time_string_to_datetime(time_string):
    hour_parts = time_string.split(':')
    hour, minute = [int(part) for part in hour_parts]
    return datetime.combine(date.today(), time(hour=hour, minute=minute))


class TimeField(object):

    def __init__(self, field):
        self.field = field

    def resolve(self, result_dict):
        return time_string_to_datetime(result_dict[self.field])


class TupleField(object):
    def __init__(self, field, tuple_class):
        self.field = field
        self.tuple_class = tuple_class

    def resolve(self, result_dict):
        return self.tuple_class.from_dict(result_dict[self.field])


class TupleListField(object):
    def __init__(self, field, tuple_class):
        self.field = field
        self.tuple_class = tuple_class

    def resolve(self, result_dict):
        return [self.tuple_class.from_dict(internal_dict)
                for internal_dict in result_dict[self.field]]


Line = build_tuple_class('Line', {
    'code': 'CodigoLinha',
    'circular': 'Circular',
    'sign': 'Letreiro',
    'direction': 'Sentido',
    'type': 'Tipo',
    'main_to_sec': 'DenominacaoTPTS',
    'sec_to_main': 'DenominacaoTSTP',
    'info': 'Informacoes',
})
Stop = build_tuple_class('Stop', {
    'code': 'CodigoParada',
    'name': 'Nome',
    'address': 'Endereco',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
})
Lane = build_tuple_class('Lane', {
    'code': 'CodCorredor',
    'cot': 'CodCot',
    'name': 'Nome',
})
Vehicle = build_tuple_class('Vehicle', {
    'plate': 'p',
    'accessible': 'a',
    'latitude': 'py',
    'longitude': 'px',
})
VehicleForecast = build_tuple_class('VehicleForecast', {
    'plate': 'p',
    'accessible': 'a',
    'arriving_at': TimeField('t'),
    'latitude': 'py',
    'longitude': 'px',
})
Positions = build_tuple_class('Positions', {
    'time': TimeField('hr'),
    'vehicles': TupleListField('vs', Vehicle),
})
LineWithVehicles = build_tuple_class('LineWithVehicles', {
    'sign': 'c',
    'code': 'cl',
    'direction': 'sl',
    'main_to_sec': 'lt0',
    'sec_to_main': 'lt1',
    'arrival_quantity': 'qv',
    'vehicles': TupleListField('vs', VehicleForecast),
})
StopWithLines = build_tuple_class('StopWithLines', {
    'code': 'cp',
    'name': 'np',
    'latitude': 'py',
    'longitude': 'px',
    'lines': TupleListField('l', LineWithVehicles),
})
ForecastWithStop = build_tuple_class('ForecastWithStop', {
    'time': TimeField('hr'),
    'stop': TupleField('p', StopWithLines),
})


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
