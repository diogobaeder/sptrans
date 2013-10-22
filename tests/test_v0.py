import json
import os
from unittest import TestCase, skipUnless
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from mock import patch
from nose.tools import istest


from . import test_fixtures
from sptrans.v0 import (
    BASE_URL,
    Client,
    Line,
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
    def searches_lines_retrieves_from_correct_url(self):
        with patch('sptrans.v0.requests') as mock_requests:
            keywords = 'my search'

            mock_requests.get.return_value.content = test_fixtures.LINE_SEARCH

            list(self.client.search_lines(keywords))

            query_string = urlencode({'termosBusca': keywords})
            url = '{}/Linha/Buscar?{}'.format(BASE_URL, query_string)
            mock_requests.get.assert_called_once_with(url, cookies=self.client.cookies)


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
