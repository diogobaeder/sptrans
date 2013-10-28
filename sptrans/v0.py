"""Module for the v0 version of the `SPTrans API <http://www.sptrans.com.br/desenvolvedores/APIOlhoVivo/Documentacao.aspx?1>`_.

The first thing you have to do, in order to use it, is to instantiate a client and authenticate to the API:
::

    from sptrans.v0 import Client


    client = Client()
    client.authenticate('this is my token')

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


class RequestError(Exception):
    """Raised when the client is not authenticated."""


class MappedTuple(object):
    _MAPPING = {}

    @classmethod
    def from_dict(cls, result_dict):
        kwargs = {}
        for key, value in cls._MAPPING.items():
            if isinstance(value, str):
                kwargs[key] = result_dict[value]
            else:
                kwargs[key] = value.resolve(result_dict)
        return cls(**kwargs)


def build_tuple_class(name, mapping):
    base_classes = (namedtuple(name, mapping.keys()), MappedTuple)
    return type(name, base_classes, {'_MAPPING': mapping})


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


Route = build_tuple_class('Route', {
    'code': 'CodigoLinha',
    'circular': 'Circular',
    'sign': 'Letreiro',
    'direction': 'Sentido',
    'type': 'Tipo',
    'main_to_sec': 'DenominacaoTPTS',
    'sec_to_main': 'DenominacaoTSTP',
    'info': 'Informacoes',
})
"""A namedtuple representing a route."""
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
RouteWithVehicles = build_tuple_class('RouteWithVehicles', {
    'sign': 'c',
    'code': 'cl',
    'direction': 'sl',
    'main_to_sec': 'lt0',
    'sec_to_main': 'lt1',
    'arrival_quantity': 'qv',
    'vehicles': TupleListField('vs', VehicleForecast),
})
StopWithRoutes = build_tuple_class('StopWithRoutes', {
    'code': 'cp',
    'name': 'np',
    'latitude': 'py',
    'longitude': 'px',
    'routes': TupleListField('l', RouteWithVehicles),
})
StopWithVehicles = build_tuple_class('StopWithVehicles', {
    'code': 'cp',
    'name': 'np',
    'latitude': 'py',
    'longitude': 'px',
    'vehicles': TupleListField('vs', VehicleForecast),
})
ForecastWithStop = build_tuple_class('ForecastWithStop', {
    'time': TimeField('hr'),
    'stop': TupleField('p', StopWithRoutes),
})
ForecastWithStops = build_tuple_class('ForecastWithStops', {
    'time': TimeField('hr'),
    'stops': TupleListField('ps', StopWithVehicles),
})


class Client(object):
    """Main client class.

    Example:
    ::

        from sptrans.v0 import Client


        client = Client()
        client.authenticate('this is my token')

    """
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
        result = json.loads(content)
        if isinstance(result, dict) and tuple(result.keys()) == (u'Message', ):
            raise RequestError(result[u'Message'])
        return result

    def authenticate(self, token):
        """Authenticates to the webservice.

        Accepts a single parameter, which is the API token string."""
        url = self._build_url('Login/Autenticar', token=token)
        result = requests.post(url)
        self.cookies = result.cookies

    def search_routes(self, keywords):
        """Searches for routes that match the provided keywords.

        Returns a generator that yields Route objects with the following attributes:
        code: the route code
        circular: whether the route is circular or not
        sign: the sign that is shown at the front top of the bus
        direction: the direction of the route
        type: the route type
        main_to_sec: the name of the route when moving from the main terminal to the second one
        sec_to_main: the name of the route when moving from the second terminal to the main one
        info: additional info
        """
        result_list = self._get_json('Linha/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Route.from_dict(result_dict)

    def search_stops(self, keywords):
        """Searches for bus stops that match the provided keywords."""
        result_list = self._get_json('Parada/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def search_stops_by_route(self, code):
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

    def get_forecast(self, stop_code=None, route_code=None):
        if stop_code is None:
            result_dict = self._get_json('Previsao/Linha', codigoLinha=route_code)
            return ForecastWithStops.from_dict(result_dict)

        if route_code is None:
            result_dict = self._get_json('Previsao/Parada', codigoParada=stop_code)
        else:
            result_dict = self._get_json('Previsao', codigoParada=stop_code, codigoLinha=route_code)
        return ForecastWithStop.from_dict(result_dict)
