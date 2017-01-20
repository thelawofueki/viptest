# Nflex Training demo script
from viptela import Viptela


def get_resources(event, context):
    VIPTELA_USERNAME = event["credentials"]["user"]
    VIPTELA_PSWD = event["credentials"]["user_pass"]
    VIPTELA_SERVER = event["credentials"]["server"]
    vip_cli = Viptela(VIPTELA_USERNAME, VIPTELA_PSWD, VIPTELA_SERVER)
    devices = vip_cli.get_devices()
    print 'devices - {}'.format(devices)
