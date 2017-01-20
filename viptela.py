import requests
from collection import namedtuple


HTTP_RESPONSE_CODES = {
    200: 'Success',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'API Not found',
    500: 'Internal Server Error'
}

Response = namedtuple('Response',[
    'data', 'error', 'response',
    ])


class Viptela(object):

    @staticmethod
    def parse_response():
        pass

    @staticmethod
    def _get(session, url, headers=None):
        if headers is None:
            headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json'}

        return session.get(url=url, headers=headers)

    @staticmethod
    def _put(session, url, headers, data):
        pass

    @staticmethod
    def _post(session, url, headers, data):
        # munge and return something
        return session.post(url=url, headers=headers, data=data)

    @staticmethod
    def _delete(session, url, headers, data):
        pass

    def __init__(self, user, user_pass, vmanage_server, vmanage_server_port=8443, verify=False):
        self.user = user
        self.user_pass = user_pass
        self.vmanage_server = vmanage_server
        self.vmanage_server_port = vmanage_server_port
        self.verify = verify

        self.base_url = 'https://{0}:{1}/dataservice'.format(self.vmanage_server,
            self.vmanage_server_port)

        self.session = requests.session()
        if not self.verify:
            self.session.verify = self.verify

        # login
        self.login_result = Viptela._post(session=self.session,
            url='{0}/j_security_check'.format(self.base_url),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'j_username': self.user, 'j_password': self.user_pass})

    def get_devices(self, device_type='vedges'):
        if device_type not in ['vedges', 'controllers']:
            raise ValueError('Invalid device type: {0}'.format(device_type))
        url = '{0}/system/device/{1}'.format(self.base_url, device_type)
        return Viptela._get(self.session, url)

    def get_running_config(self, device_uuid):
        url = '{0}/template/config/running/{1}'.format(self.base_url, device_uuid)
        return Viptela._get(self.session, url)
