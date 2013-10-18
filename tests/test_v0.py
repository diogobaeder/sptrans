from mock import patch
from nose.tools import istest
from unittest import TestCase


from sptrans.v0 import BASE_URL, Client


class ClientTest(TestCase):

    @istest
    @patch('sptrans.v0.requests')
    def authenticates_the_user(self, mock_requests):
        token = 'some token'
        client = Client()

        client.Autenticar(token)

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

        client.Autenticar(token)

        self.assertEqual(client.cookies, response.cookies)
