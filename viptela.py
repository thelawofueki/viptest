import requests
from collections import namedtuple


HTTP_RESPONSE_CODES = {
    200: 'Success',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'API Not found',
    500: 'Internal Server Error'
}

Response = namedtuple('Response', [
    'data', 'error', 'response',
    ])


class Viptela(object):

    def parse_response():
        pass

    def _get(self, url, headers=None):
        if headers is None:
            headers = {
                'Connection': 'keep-alive',
                'Content-Type': 'application/json'
            }
        return self.session.get(url=url, headers=headers)

    def _put(self, url, headers, data):
        return self.session.put(url=url, headers=headers, data=data)

    def _post(self, url, headers, data):
        # munge and return something
        return self.session.post(url=url, headers=headers, data=data)

    def _delete(self, url, headers, data):
        return self.session.delete(url=url, headers=headers, data=data)

    def __init__(self,
                 user,
                 user_pass,
                 vmanage_server,
                 vmanage_server_port=443,
                 verify=False):
        self.user = user
        self.user_pass = user_pass
        self.vmanage_server = vmanage_server
        self.vmanage_server_port = vmanage_server_port
        self.verify = verify

        self.base_url = 'https://{0}/dataservice'.format(
            self.vmanage_server, self.vmanage_server_port
        )

        self.session = requests.session()
        if not self.verify:
            self.session.verify = self.verify

        # login
        self.login_result = self._post(
            url='{0}/j_security_check'.format(self.base_url),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'j_username': self.user, 'j_password': self.user_pass}
        )

    def get_devices(self, device_type='vedges'):
        if device_type not in ['vedges', 'controllers']:
            raise ValueError('Invalid device type: {0}'.format(device_type))
        url = '{0}/system/device/{1}'.format(self.base_url, device_type)
        response = self._get(url).json()
        try:
            return response["data"]

        except KeyError:
            raise Exception("No data fetched from Viptela")

    def get_running_config(self, device_uuid):
        url = '{0}/template/config/running/{1}'.format(
            self.base_url, device_uuid
        )
        return self._get(url)

    def get_device_maps(self):
        url = '{0}/group/map/devices'
        response = self._get(url).json()
        try:
            return response["data"]

        except KeyError:
            raise Exception("No data fetched from Viptela")