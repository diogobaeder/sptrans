import json

from mock import patch
from nose.tools import istest
from unittest import TestCase


from . import test_fixtures
from sptrans.v0 import (
    BASE_URL,
    Client,
    Line,
)


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
    @patch('sptrans.v0.requests')
    def authenticates_the_user(self, mock_requests):
        token = 'some token'
        client = Client()

        client.authenticate(token)

        expected_url = '{}/Login/Autenticar?token={}'.format(BASE_URL, token)
        mock_requests.post.assert_called_once_with(expected_url)

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
                          for line_dict in json.loads(test_fixtures.LINE_SEARCH)]
        self.assertEqual(lines, expected_lines)

    @istest
    @patch('sptrans.v0.requests')
    def searches_lines_returns_generator(self, mock_requests):
        keywords = 'my search'

        mock_requests.get.return_value.content = test_fixtures.LINE_SEARCH

        lines = self.client.search_lines(keywords)

        self.assert_is_a_generator(lines)


class LineTest(TestCase):

    @istest
    def converts_a_dict_to_a_line(self):
        line_dict = json.loads(test_fixtures.LINE_SEARCH)[0]

        line = Line.from_dict(line_dict)

        self.assertEqual(line.code, 1273)
        self.assertEqual(line.circular, False)
        self.assertEqual(line.sign, '8000')
        self.assertEqual(line.direction, 1)
        self.assertEqual(line.type, 10)
        self.assertEqual(line.main_to_sec, 'PCA.RAMOS DE AZEVEDO')
        self.assertEqual(line.sec_to_main, 'TERMINAL LAPA')
        self.assertEqual(line.info, None)
