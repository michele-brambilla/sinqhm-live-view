from .error import CommunicationError

import requests
from requests.auth import HTTPBasicAuth
import numpy as np


class Connector(object):
    def get(self, path):
        pass


class HttpConnector(Connector):
    parameters = {}

    status_code_msg = {
        400: 'Bad request',
        403: 'Authentication did not work..',
        404: 'Somehow, address was not found!',
        500: 'Internal server error',
    }

    def __init__(self, URL, Authorization, Endianness='little', demo=None):
        self.parameters['baseurl'] = URL
        self.parameters['endianness'] = Endianness
        self.parameters['user'] = Authorization.name
        self.parameters['password'] = Authorization.password
        self.demo = demo
        self.shape = [10, 100]

    def _basic_request(self, name):
        req = 'http://' + self.parameters['baseurl'] + name
        return req

    def _authorization(self):
        return HTTPBasicAuth(self.parameters['user'], self.parameters['password'])

    def get_raw(self, name='/admin/readhmdata.egi?bank=0'):
        """Connect to *baseurl/name* using the GET protocol
        :param name: String to be appended to the *baseurl*
        :param params: GET parameters to be passed
        :return: (requests.Response) response
        """
        req = self._basic_request(name)
        auth = self._authorization()
        r = requests.get(req, auth=auth)
        if r.status_code != requests.codes.ok:
            raise CommunicationError('HTTP request failure')
        return r

    def _get_axis_length(self, r):
        tag_open = '<td>'
        tag_close = '</td>'
        _axis_length = []

        for line in r.iter_lines():
            l = str(line)
            if 'Length' in l:
                first = l.find(tag_open) + len(tag_open)
                last = l.find(tag_close)
                _axis_length.append(int(l[first:last]))
        return _axis_length

    def get_shape(self, name='/admin/showconfig.egi?bank=0'):
        if not self.demo:
            config = self.get_raw(name)
            self.shape = self._get_axis_length(config)[:-1]
        return self.shape

    def get(self, name='/admin/readhmdata.egi?bank=0'):
        if self.demo:
            return np.random.randint(0, 100, np.prod(self.shape))
        content = self.get_raw(name).content
        if self.parameters['endianness'] is not 'little':
            content.byteswap()
        return np.frombuffer(content, dtype=np.uint32)


class RawFileConnector(Connector):
    parameters = {}

    def __init__(self, Filename, Endianness='little'):
        self.parameters["filename"] = Filename
        self.parameters['endianness'] = Endianness

    def get(self, path):
        content = np.fromfile(self.parameters["filename"], dtype=np.float32)
        if self.parameters['endianness'] is not 'little':
            content.byteswap()
        return content
