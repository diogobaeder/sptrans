import requests


BASE_URL = 'http://api.olhovivo.sptrans.com.br/v0'


class Client(object):
    cookies = None

    def Autenticar(self, token):
        result = requests.post('{}/Login/Autenticar?token={}'.format(BASE_URL, token))
        self.cookies = result.cookies
