# Nflex Training demo script
from datetime import datetime
from uuid import uuid4
from viptela import Viptela


def get_resources(event, context):
    VIPTELA_USERNAME = event["credentials"]["username"]
    VIPTELA_PSWD = event["credentials"]["password"]
    VIPTELA_SERVER = "54.251.162.192"
    vip_cli = Viptela(VIPTELA_USERNAME, VIPTELA_PSWD, VIPTELA_SERVER)
    devices = vip_cli.get_devices()
    print "Fetched %d resources from Viptela" % len(devices)
    return list(format_resources(devices))


def format_resources(resources):
    for resource in resources:
        yield format_resource(resource)


def format_resource(resource):
    state = (
        "running" if resource.get("deviceState") == "valid" else "unknown"
    )
    return {
        'base': {
            'name': 'ncsDeviceName 1',
            'provider_created_at': datetime.utcnow().isoformat() + "Z"
        },
        'id': str(uuid4()),
        'type': 'server',
        'details': {
            'server': {
                "state": state,
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
            "provider_specific": {
                "deviceModel": resource.get("deviceModel", ""),
                "deviceState": resource.get("deviceState", ""),
                "chasisNumber": resource.get("chasisNumber", ""),
                "uuid": resource.get("uuid", ""),
                "serialNumber": resource.get("serialNumber", ""),
                "site-id": resource.get("site-id", ""),
            },
        }
    }
