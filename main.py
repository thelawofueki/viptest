# Nflex Training demo script
from datetime import datetime
from uuid import uuid4
from viptela import Viptela


def get_resources(event, context):
    VIPTELA_USERNAME = event["credentials"]["user"]
    VIPTELA_PSWD = event["credentials"]["user_pass"]
    VIPTELA_SERVER = event["credentials"]["server"]
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
    return {
        'base': {
            'name': 'ncsDeviceName 1',
            'provider_created_at': datetime.utcnow().isoformat() + "Z"
        },
        'id': str(uuid4()),
        'type': 'server',
        'details': {
            'server': {
                "template": {
                    "id": resource.get("templateId", ""),
                    "name": resource.get("template", ""),
                },
                "ip_addresses": [
                    {
                        "ip_address": resource.get("deviceIP", "N/A"),
                        "description": "deviceIP",
                    },
                    {
                        "ip_address": resource.get("system-ip", "N/A"),
                        "description": "system-ip",
                    },
                    {
                        "ip_address": resource.get("vbond", "N/A"),
                        "description": "vbond",
                    },
                ]
            },
        },
        "metadata": {
            "deviceModel": resource.get("deviceModel", ""),
            "deviceState": resource.get("deviceState", ""),
            "chasisNumber": resource.get("chasisNumber", ""),
            "uuid": resource.get("uuid", ""),
            "serialNumber": resource.get("serialNumber", ""),
            "site-id": resource.get("site-id", ""),

        }
    }
