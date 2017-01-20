# Nflex Training demo script
from viptela import Viptela  # noqa


def get_resources(event, context):
    VIPTELA_USERNAME = event["credentials"]["user"]
    VIPTELA_PSWD = event["credentials"]["user_pass"]
    VIPTELA_SERVER = event["credentials"]["server"]
    print VIPTELA_USERNAME, VIPTELA_PSWD, VIPTELA_SERVER
    # vip_cli = Viptela(VIPTELA_USERNAME, VIPTELA_PSWD, VIPTELA_SERVER)
    # devices = vip_cli.get_devices()
    devices = [
        {
            "deviceIP": "1.1.1.0",
            "device-model": "vedge-1000",
            "host-name": "LAB_VE1",
            "serialNumber": "10001106",
        },
        {
            "deviceIP": "10.1.1.20",
            "device-model": "hostvedge-100-WM",
            "host-name": "JG-VE-HOME",
            "serialNumber": "10009E34",
        },
        {
            "deviceIP": "10.1.1.30",
            "device-model": "vedge-cloud",
            "host-name": "JG-VE-CLOUD",
            "serialNumber": "17A4459533462B5478819BAC03D17D49",
        },
    ]
    print "Fetched %d resources from Viptela" % len(devices)
    return list(format_resources(devices))


def format_resources(resources):
    for resource in resources:
        yield format_resource(resource)


def format_resource(resource):
    print resource
    resource.get('deviceIP', ''),
    resource.get('device-model', ''),
    resource.get('host-name', ''),
    resource.get('serialNumber', '')
    return {
        'base': {
            'name': 'Server 1',
            'provider_created_at': '2017-01-01T12:00:00.000000Z'
        },
        'id': '00000000-0000-0000-0000-100000000001',
        'type': 'network',
        'details': {
            'server': {
            },
        },
    }
