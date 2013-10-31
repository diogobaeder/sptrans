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
    """Raised when the request failes to be accomplished.

    Normally this is due to the client not being authenticated anymore.
    In this case, just authenticate again, and it should be back at work.
    """


class AuthenticationError(Exception):
    """Raised when the authentication fails - for example, with a wrong token -."""


class _TupleMapMixin(object):
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


def _build_tuple_class(name, mapping):
    base_classes = (namedtuple(name, mapping.keys()), _TupleMapMixin)
    return type(name, base_classes, {'_MAPPING': mapping})


def _time_string_to_datetime(time_string):
    hour_parts = time_string.split(':')
    hour, minute = [int(part) for part in hour_parts]
    return datetime.combine(date.today(), time(hour=hour, minute=minute))


class _TimeField(object):

    def __init__(self, field):
        self.field = field

    def resolve(self, result_dict):
        return _time_string_to_datetime(result_dict[self.field])


class _TupleField(object):
    def __init__(self, field, tuple_class):
        self.field = field
        self.tuple_class = tuple_class

    def resolve(self, result_dict):
        return self.tuple_class.from_dict(result_dict[self.field])


class _TupleListField(object):
    def __init__(self, field, tuple_class):
        self.field = field
        self.tuple_class = tuple_class

    def resolve(self, result_dict):
        return [self.tuple_class.from_dict(internal_dict)
                for internal_dict in result_dict[self.field]]


Route = _build_tuple_class('Route', {
    'code': 'CodigoLinha',
    'circular': 'Circular',
    'sign': 'Letreiro',
    'direction': 'Sentido',
    'type': 'Tipo',
    'main_to_sec': 'DenominacaoTPTS',
    'sec_to_main': 'DenominacaoTSTP',
    'info': 'Informacoes',
})
"""A namedtuple representing a route.

:var code: (:class:`int`) The route code.
:var circular: (:class:`bool`) Wether it's a circular route or not (without a secondary terminal).
:var sign: (:class:`str`) The first part of the route sign.
:var direction: (:class:`int`) The route direction. "1" means "main to secondary terminal", "2" means "secondary to main terminal".
:var type: (:class:`int`) The route type.
:var main_to_sec: (:class:`str`) The name of the route when moving from the main terminal to the second one.
:var sec_to_main: (:class:`str`) The name of the route when moving from the second terminal to the main one.
:var info: (:class:`str`) Extra information about the route.
"""
Stop = _build_tuple_class('Stop', {
    'code': 'CodigoParada',
    'name': 'Nome',
    'address': 'Endereco',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
})
"""A namedtuple representing a bus stop.

:var code: (:class:`int`) The stop code.
:var name: (:class:`str`) The stop name.
:var address: (:class:`str`) The stop address.
:var latitude: (:class:`float`) The stop latitude.
:var longitude: (:class:`float`) The stop longitude.
"""
Lane = _build_tuple_class('Lane', {
    'code': 'CodCorredor',
    'cot': 'CodCot',
    'name': 'Nome',
})
"""A namedtuple representing a bus lane.

:var code: (:class:`int`) The lane code.
:var cot: (:class:`int`) The lane "cot" (?).
:var name: (:class:`str`) The lane name.
"""
Vehicle = _build_tuple_class('Vehicle', {
    'prefix': 'p',
    'accessible': 'a',
    'latitude': 'py',
    'longitude': 'px',
})
"""A namedtuple representing a vehicle (bus) with its position.

:var prefix: (:class:`str`) The vehicle prefix painted in the bus.
:var accessible: (:class:`bool`) Wether the vehicle is accessible or not.
:var latitude: (:class:`float`) The vehicle latitude.
:var longitude: (:class:`float`) The vehicle longitude.
"""
VehicleForecast = _build_tuple_class('VehicleForecast', {
    'prefix': 'p',
    'accessible': 'a',
    'arriving_at': _TimeField('t'),
    'latitude': 'py',
    'longitude': 'px',
})
"""A namedtuple representing a vehicle (bus) with its position and forecast to arrive at a certain stop.

:var prefix: (:class:`str`) The vehicle prefix painted in the bus.
:var accessible: (:class:`bool`) Wether the vehicle is accessible or not.
:var arriving_at: (:class:`datetime.datetime`) The time that the vehicle is expected to arrive.
:var latitude: (:class:`float`) The vehicle latitude.
:var longitude: (:class:`float`) The vehicle longitude.
"""
Positions = _build_tuple_class('Positions', {
    'time': _TimeField('hr'),
    'vehicles': _TupleListField('vs', Vehicle),
})
"""A namedtuple representing a sequence of vehicles positions, with the time when the information was retrieved.

:var time: (:class:`datetime.datetime`) The time when the information was retrieved.
:var vehicles: (:class:`list`) The list of :class:`vehicles <Vehicle>`.
"""
RouteWithVehicles = _build_tuple_class('RouteWithVehicles', {
    'sign': 'c',
    'code': 'cl',
    'direction': 'sl',
    'main_to_sec': 'lt0',
    'sec_to_main': 'lt1',
    'quantity': 'qv',
    'vehicles': _TupleListField('vs', VehicleForecast),
})
"""A namedtuple representing a route with a sequence of vehicles with their current positions.

:var sign: (:class:`str`) The first part of the route sign.
:var code: (:class:`int`) The route code.
:var direction: (:class:`int`) The route direction. "1" means "main to secondary terminal", "2" means "secondary to main terminal".
:var main_to_sec: (:class:`str`) The name of the route when moving from the main terminal to the second one.
:var sec_to_main: (:class:`str`) The name of the route when moving from the second terminal to the main one.
:var quantity: (:class:`int`) The quantity of vehicles.
:var vehicles: (:class:`list`) The list of :class:`vehicles <Vehicle>`.
"""
StopWithRoutes = _build_tuple_class('StopWithRoutes', {
    'code': 'cp',
    'name': 'np',
    'latitude': 'py',
    'longitude': 'px',
    'routes': _TupleListField('l', RouteWithVehicles),
})
"""A namedtuple representing a bus stop with a list of routes that pass through this stop.

:var code: (:class:`int`) The stop code.
:var name: (:class:`str`) The stop name.
:var latitude: (:class:`float`) The stop latitude.
:var longitude: (:class:`float`) The stop longitude.
:var routes: (:class:`list`) The list of :class:`routes <Route>` that pass through this stop.
"""
StopWithVehicles = _build_tuple_class('StopWithVehicles', {
    'code': 'cp',
    'name': 'np',
    'latitude': 'py',
    'longitude': 'px',
    'vehicles': _TupleListField('vs', VehicleForecast),
})
"""A namedtuple representing a bus stop with a list of vehicles that pass through this stop.

:var code: (:class:`int`) The stop code.
:var name: (:class:`str`) The stop name.
:var latitude: (:class:`float`) The stop latitude.
:var longitude: (:class:`float`) The stop longitude.
:var vehicles: (:class:`list`) The list of :class:`vehicles <Vehicle>`.
"""
ForecastWithStop = _build_tuple_class('ForecastWithStop', {
    'time': _TimeField('hr'),
    'stop': _TupleField('p', StopWithRoutes),
})
"""A namedtuple representing a bus stop forecast with routes and the time when the information was retrieved.

:var time: (:class:`datetime.datetime`) The time when the information was retrieved.
:var stop: (:class:`StopWithRoutes`) The bus stop with :class:`routes <Route>`.
"""
ForecastWithStops = _build_tuple_class('ForecastWithStops', {
    'time': _TimeField('hr'),
    'stops': _TupleListField('ps', StopWithVehicles),
})
"""A namedtuple representing a list of bus stops forecast with vehicles and the time when the information was retrieved.

:var time: (:class:`datetime.datetime`) The time when the information was retrieved.
:var stops: (:class:`list` of :class:`StopWithVehicles`) The bus stops.
"""


class Client(object):
    """Main client class.

    .. warning:: Any method (except :meth:`authenticate`) may raise :class:`RequestError` if the client is not authenticated anymore.
       So keep an eye on the authentication state.

    Example:
    ::

        from sptrans.v0 import Client


        client = Client()
        client.authenticate('this is my token')

    """
    _cookies = None

    def _build_url(self, endpoint, **kwargs):
        query_string = urlencode(kwargs)
        return '{}/{}?{}'.format(BASE_URL, endpoint, query_string)

    def _get_content(self, endpoint, **kwargs):
        url = self._build_url(endpoint, **kwargs)
        response = requests.get(url, cookies=self._cookies)
        return response.content.decode('latin1')

    def _get_json(self, endpoint, **kwargs):
        content = self._get_content(endpoint, **kwargs)
        result = json.loads(content)
        if isinstance(result, dict) and tuple(result.keys()) == (u'Message', ):
            raise RequestError(result[u'Message'])
        return result

    def authenticate(self, token):
        """Authenticates to the webservice.

        :param token: The API token string.
        :type token: :class:`str`
        :raises: :class:`AuthenticationError` when there's an error during authentication.
        """
        url = self._build_url('Login/Autenticar', token=token)
        response = requests.post(url)
        result = json.loads(response.content.decode('latin1'))
        if not result:
            raise AuthenticationError('Cannot authenticate with token "{}"'.format(token))
        self._cookies = response.cookies

    def search_routes(self, keywords):
        """Searches for routes that match the provided keywords.

        :param keywords: The keywords, in a single string, to use for matching.
        :type keywords: :class:`str`
        :return: A generator that yields :class:`Route` objects.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')
            for route in client.search_routes('butanta'):
                print(route.code, route.sign)

        """
        result_list = self._get_json('Linha/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Route.from_dict(result_dict)

    def search_stops(self, keywords):
        """Searches for bus stops that match the provided keywords.

        :param keywords: The keywords, in a single string, to use for matching.
        :type keywords: :class:`str`
        :return: A generator that yields :class:`Stop` objects.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')
            for stop in client.search_stops('butanta'):
                print(stop.code, stop.name)
        """
        result_list = self._get_json('Parada/Buscar', termosBusca=keywords)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def search_stops_by_route(self, code):
        """Searches for bus stops that are passed by the route specified by its code.

        :param code: The route code to use for matching.
        :type code: :class:`int`
        :return: A generator that yields :class:`Stop` objects.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')
            for stop in client.search_stops_by_route(1234):
                print(stop.code, stop.name)
        """
        result_list = self._get_json('Parada/BuscarParadasPorLinha', codigoLinha=code)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def search_stops_by_lane(self, code):
        """Searches for bus stops that are contained in a lane specified by its code.

        :param code: The lane code to use for matching.
        :type code: :class:`int`
        :return: A generator that yields :class:`Stop` objects.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')
            for stop in client.search_stops_by_lane(1234):
                print(stop.code, stop.name)
        """
        result_list = self._get_json('Parada/BuscarParadasPorCorredor', codigoCorredor=code)
        for result_dict in result_list:
            yield Stop.from_dict(result_dict)

    def list_lanes(self):
        """Lists all the bus lanes in the city.

        :return: A generator that yields :class:`Lane` objects.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')
            for lane in client.list_lanes():
                print(lane.code, lane.name)
        """
        result_list = self._get_json('Corredor')
        for result_dict in result_list:
            yield Lane.from_dict(result_dict)

    def get_positions(self, code):
        """Gets the vehicles with their current positions, provided a route code.

        :param code: The route code to use for matching.
        :type code: :class:`int`
        :return: A single :class:`Positions` object.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')

            positions = client.get_positions(1234)
            print(positions.time)

            for vehicle in positions.vehicles:
                print(vehicle.prefix)
        """
        result_dict = self._get_json('Posicao', codigoLinha=code)
        return Positions.from_dict(result_dict)

    def get_forecast(self, stop_code=None, route_code=None):
        """Gets the arrival forecast, provided a route code or a stop code or both.

        You must provide at least one of the parameters.
        If you provide only a `stop_code`, it will return a forecast for all routes that attend a certain stop.
        If you provide only a `route_code`, it will return a forecast for all stops that a certain route attends to.
        If you provide both, it will return a forecast for the specific route attending to the specific stop provided.

        :param stop_code: The stop code to use for matching.
        :type stop_code: :class:`int`
        :param route_code: The stop code to use for matching.
        :type route_code: :class:`int`
        :return: A single :class:`ForecastWithStop` object, when passing only `stop_code` or both.
        :return: A single :class:`ForecastWithStops` object, when passing only `route_code`.

        Example:
        ::

            from sptrans.v0 import Client


            client = Client()
            client.authenticate('this is my token')

            forecast = client.get_forecast(stop_code=1234)
            for route in forecast.stop.routes:
                for vehicle in route.vehicles:
                    print(vehicle.prefix)

            forecast = client.get_forecast(stop_code=1234, route_code=2345)
            for route in forecast.stop.routes:
                for vehicle in route.vehicles:
                    print(vehicle.prefix)

            forecast = client.get_forecast(route_code=2345)
            for stop in forecast.stops:
                for vehicle in stop.vehicles:
                    print(vehicle.prefix)
        """
        if stop_code is None:
            result_dict = self._get_json('Previsao/Linha', codigoLinha=route_code)
            return ForecastWithStops.from_dict(result_dict)

        if route_code is None:
            result_dict = self._get_json('Previsao/Parada', codigoParada=stop_code)
        else:
            result_dict = self._get_json('Previsao', codigoParada=stop_code, codigoLinha=route_code)
        return ForecastWithStop.from_dict(result_dict)
