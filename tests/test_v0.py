# -*- coding: utf-8 -*-
import json
import os
from unittest import TestCase, skipUnless

from mock import patch
from nose.tools import istest


from . import test_fixtures
from sptrans.v0 import (
    BASE_URL,
    Client,
    Line,
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

        url = self.client.build_url('foo/bar', baz='john doe')

        self.assertEqual(url, expected_url)

    @istest
    @patch('sptrans.v0.requests')
    def gets_content_from_a_certain_endpoint(self, mock_requests):
        url = '{}/foo/bar?baz=joe'.format(BASE_URL)
        content = u'some façade'
        mock_requests.get.return_value.content = content.encode('latin1')

        content = self.client.get_content('foo/bar', baz='joe')

        self.assertEqual(content, content)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def authenticates_the_user(self, mock_requests):
        token = 'some token'
        client = Client()

        client.authenticate(token)

        url = self.client.build_url('Login/Autenticar', token=token)
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
        self.assertEqual(lines, expected_lines)

    @istest
    @patch('sptrans.v0.requests')
    def searches_lines_returns_generator(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.LINE_SEARCH

        lines = self.client.search_lines(keywords)

        self.assert_is_a_generator(lines)

    @istest
    @patch('sptrans.v0.requests')
    def searches_lines_retrieves_from_correct_url(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.LINE_SEARCH

        list(self.client.search_lines(keywords))

        url = self.client.build_url('Linha/Buscar', termosBusca=keywords)
        mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)

    @istest
    @patch('sptrans.v0.requests')
    def searches_stops(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.STOP_SEARCH

        stops = list(self.client.search_stops(keywords))

        expected_stops = [Stop.from_dict(stop_dict)
                          for stop_dict in json.loads(test_fixtures.STOP_SEARCH.decode('latin1'))]
        self.assertEqual(stops, expected_stops)


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
