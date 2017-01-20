# Nflex Training demo script
from datetime import datetime
from viptela import Viptela
import metrics


def get_metrics(event, context):
    return metrics.get_metrics(event, context)


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
        try:
            yield format_resource(resource)
        except KeyError:
            continue


def format_resource(resource):
    state = (
        "running" if resource.get("deviceState") == "valid" else "unknown"
    )
    return {
        'base': {
            'name': resource.get("host-name"),
            'provider_created_at': datetime.utcnow().isoformat() + "Z"
        },
        'id': resource["deviceIP"],
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
