# -*- coding: utf-8 -*-
from datetime import date, datetime, time
import json
import os
from unittest import TestCase, skipUnless

from mock import patch
from nose.tools import istest


from . import test_fixtures
from sptrans.v0 import (
    BASE_URL,
    Client,
    ForecastWithStop,
    Lane,
    Line,
    Positions,
    Stop,
)


TOKEN = os.environ.get('SPTRANS_TOKEN', None)


class ClientTest(TestCase):

    client = None

    def setUp(self):
        self.client = Client()
        self.client.cookies = 'some cookies for later'

    def assert_is_a_generator(self, obj):
        foo = (_ for _ in [])
        generator_type = type(foo)
        self.assertIsInstance(obj, generator_type)

    @istest
    def builds_a_usable_url_from_endpoint_and_parameters(self):
        expected_url = '{}/foo/bar?baz=john+doe'.format(BASE_URL)

        url = self.client._build_url('foo/bar', baz='john doe')

        self.assertEqual(url, expected_url)

    @istest
    @patch('sptrans.v0.requests')
    def gets_content_from_a_certain_endpoint(self, mock_requests):
        url = '{}/foo/bar?baz=joe'.format(BASE_URL)
        content = u'some façade'
        mock_requests.get.return_value.content = content.encode('latin1')

        content = self.client._get_content('foo/bar', baz='joe')

        self.assertEqual(content, content)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def authenticates_the_user(self, mock_requests):
        token = 'some token'
        client = Client()

        client.authenticate(token)

        url = self.client._build_url('Login/Autenticar', token=token)
        mock_requests.post.assert_called_once_with(url)

    @istest
    @patch('sptrans.v0.requests')
    def keeps_cookies_for_later(self, mock_requests):
        token = 'some token'
        client = Client()

        class response:
            cookies = 'some cookies'
        mock_requests.post.return_value = response

        client.authenticate(token)

        self.assertEqual(client.cookies, response.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def searches_lines(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.LINE_SEARCH

        lines = list(self.client.search_lines(keywords))

        expected_lines = [Line.from_dict(line_dict)
                          for line_dict in json.loads(test_fixtures.LINE_SEARCH.decode('latin1'))]
        url = self.client._build_url('Linha/Buscar', termosBusca=keywords)
        self.assertEqual(lines, expected_lines)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def searches_lines_returns_generator(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.LINE_SEARCH

        lines = self.client.search_lines(keywords)

        self.assert_is_a_generator(lines)

    @istest
    @patch('sptrans.v0.requests')
    def searches_stops(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.STOP_SEARCH

        stops = list(self.client.search_stops(keywords))

        expected_stops = [Stop.from_dict(stop_dict)
                          for stop_dict in json.loads(test_fixtures.STOP_SEARCH.decode('latin1'))]
        url = self.client._build_url('Parada/Buscar', termosBusca=keywords)
        self.assertEqual(stops, expected_stops)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def searches_stops_by_line(self, mock_requests):
        code = '1234'

        mock_requests.get.return_value.content = test_fixtures.STOP_SEARCH_BY_LINE

        stops = list(self.client.search_stops_by_line(code))

        expected_stops = [Stop.from_dict(stop_dict)
                          for stop_dict in json.loads(test_fixtures.STOP_SEARCH_BY_LINE.decode('latin1'))]
        url = self.client._build_url('Parada/BuscarParadasPorLinha', codigoLinha=code)
        self.assertEqual(stops, expected_stops)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def searches_stops_by_lane(self, mock_requests):
        code = '1234'

        mock_requests.get.return_value.content = test_fixtures.STOP_SEARCH_BY_LANE

        stops = list(self.client.search_stops_by_lane(code))

        expected_stops = [Stop.from_dict(stop_dict)
                          for stop_dict in json.loads(test_fixtures.STOP_SEARCH_BY_LANE.decode('latin1'))]
        url = self.client._build_url('Parada/BuscarParadasPorCorredor', codigoCorredor=code)
        self.assertEqual(stops, expected_stops)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def lists_lanes(self, mock_requests):
        mock_requests.get.return_value.content = test_fixtures.LANES

        lanes = list(self.client.list_lanes())

        expected_lanes = [Lane.from_dict(lane_dict)
                          for lane_dict in json.loads(test_fixtures.LANES.decode('latin1'))]
        url = self.client._build_url('Corredor')
        self.assertEqual(lanes, expected_lanes)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def gets_positions(self, mock_requests):
        fixture = test_fixtures.VEHICLE_POSITIONS
        code = '1234'

        mock_requests.get.return_value.content = fixture

        positions = self.client.get_positions(code)

        expected_positions = Positions.from_dict(json.loads(fixture.decode('latin1')))
        url = self.client._build_url('Posicao', codigoLinha=code)
        self.assertEqual(positions, expected_positions)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    #@istest
    #@patch('sptrans.v0.requests')
    #def gets_forecast(self, mock_requests):
        #fixture = test_fixtures.ARRIVAL_FORECAST
        #stop_code = '1234'
        #line_code = '2345'

        #mock_requests.get.return_value.content = fixture

        #forecast = self.client.get_forecast(stop_code=stop_code, line_code=line_code)

        #expected_forecast = ForecastWithStop.from_dict(json.loads(fixture.decode('latin1')))
        #url = self.client._build_url('Previsao', codigoParada=stop_code, codigoLinha=line_code)
        #self.assertEqual(forecast, expected_forecast)
        #mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)


@skipUnless(TOKEN, 'Please provide an SPTRANS_TOKEN env variable')
class ClientFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.authenticate(TOKEN)

    @istest
    def searches_lines(self):
        keywords = 'lapa'
        lines = list(self.client.search_lines(keywords))

        self.assertGreater(len(lines), 0)
        for line in lines:
            main = line.main_to_sec.lower()
            sec = line.sec_to_main.lower()
            self.assertTrue((keywords in main) or (keywords in sec))


class LineTest(TestCase):

    @istest
    def converts_a_dict_to_a_line(self):
        line_dict = json.loads(test_fixtures.LINE_SEARCH.decode('latin1'))[0]

        line = Line.from_dict(line_dict)

        self.assertEqual(line.code, 1273)
        self.assertEqual(line.circular, False)
        self.assertEqual(line.sign, '8000')
        self.assertEqual(line.direction, 1)
        self.assertEqual(line.type, 10)
        self.assertEqual(line.main_to_sec, 'PCA.RAMOS DE AZEVEDO')
        self.assertEqual(line.sec_to_main, 'TERMINAL LAPA')
        self.assertEqual(line.info, None)


class StopTest(TestCase):

    @istest
    def converts_a_dict_to_a_stop(self):
        stop_dict = json.loads(test_fixtures.STOP_SEARCH.decode('latin1'))[0]

        stop = Stop.from_dict(stop_dict)

        self.assertEqual(stop.code, 340015329)
        self.assertEqual(stop.name, "AFONSO BRAZ B/C1")
        self.assertEqual(stop.address, 'R ARMINDA/ R BALTHAZAR DA VEIGA')
        self.assertEqual(stop.latitude, -23.592938)
        self.assertEqual(stop.longitude, -46.672727)


class LaneTest(TestCase):

    @istest
    def converts_a_dict_to_a_lane(self):
        lane_dict = {
            'CodCorredor': 8,
            'CodCot': 0,
            'Nome': 'Campo Limpo',
        }

        lane = Lane.from_dict(lane_dict)

        self.assertEqual(lane.code, 8)
        self.assertEqual(lane.cot, 0)
        self.assertEqual(lane.name, 'Campo Limpo')


class PositionsTest(TestCase):

    @istest
    def converts_a_dict_to_a_positions_object_with_vehicles(self):
        positions_dict = json.loads(test_fixtures.VEHICLE_POSITIONS.decode('latin1'))
        today = date.today()
        hour = time(hour=22, minute=57)

        positions = Positions.from_dict(positions_dict)

        self.assertEqual(positions.time, datetime.combine(today, hour))

        self.assertEqual(positions.vehicles[0].plate, '11433')
        self.assertEqual(positions.vehicles[0].accessible, False)
        self.assertEqual(positions.vehicles[0].latitude, -23.540150375000003)
        self.assertEqual(positions.vehicles[0].longitude, -46.64414075)

        self.assertEqual(positions.vehicles[1].plate, '12132')
        self.assertEqual(positions.vehicles[1].accessible, False)
        self.assertEqual(positions.vehicles[1].latitude, -23.5200315)
        self.assertEqual(positions.vehicles[1].longitude, -46.699387)


class ForecastWithStopTest(TestCase):

    @istest
    def converts_a_dict_to_an_forecast_object_with_stop_lines_and_vehicles(self):
        forecast_dict = json.loads(test_fixtures.FORECAST_FOR_LINE_AND_STOP.decode('latin1'))
        today = date.today()

        forecast = ForecastWithStop.from_dict(forecast_dict)

        self.assertEqual(forecast.time, datetime.combine(today, time(hour=23, minute=9)))

        self.assertEqual(forecast.stop.code, 4200953)
        self.assertEqual(forecast.stop.name, 'PARADA ROBERTO SELMI DEI B/C')
        self.assertEqual(forecast.stop.latitude, -23.675901)
        self.assertEqual(forecast.stop.longitude, -46.752812)

        self.assertEqual(forecast.stop.lines[0].sign, '7021-10')
        self.assertEqual(forecast.stop.lines[0].code, 1989)
        self.assertEqual(forecast.stop.lines[0].direction, 1)
        self.assertEqual(forecast.stop.lines[0].main_to_sec, u'TERM. JOÃO DIAS')
        self.assertEqual(forecast.stop.lines[0].sec_to_main, u'JD. MARACÁ')
        self.assertEqual(forecast.stop.lines[0].arrival_quantity, 1)

        self.assertEqual(forecast.stop.lines[0].vehicles[0].plate, '74558')
        self.assertEqual(forecast.stop.lines[0].vehicles[0].arriving_at, datetime.combine(today, time(hour=23, minute=11)))
        self.assertEqual(forecast.stop.lines[0].vehicles[0].accessible, True)
        self.assertEqual(forecast.stop.lines[0].vehicles[0].latitude, -23.67603)
        self.assertEqual(forecast.stop.lines[0].vehicles[0].longitude, -46.75891166666667)
