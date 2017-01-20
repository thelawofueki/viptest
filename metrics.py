from datetime import datetime
from viptela import Viptela

MAPPING = {
    "rx_pkts": "network-in-packets.%s.cntr",
    "tx_pkts": "network-out-packets.%s.cntr",
}


def get_metrics(event, context):
    VIPTELA_USERNAME = event["credentials"]["username"]
    VIPTELA_PSWD = event["credentials"]["password"]
    VIPTELA_SERVER = "54.251.162.192"
    vip_cli = Viptela(VIPTELA_USERNAME, VIPTELA_PSWD, VIPTELA_SERVER)
    data = vip_cli.get_device_metrics(event["resource"]["provider_id"])
    print "Fetched %d data samples from Viptela" % len(data)
    if data:
        return list(format_metrics(data))

    return []


def format_metrics(data):
    metrics = []
    for sample in data:
        metrics += format_sample(sample)

    return metrics


def format_sample(sample):
    metrics = []
    ts = datetime.fromtimestamp(sample.get("lastupdated") / 1e3)
    for metric_name, cmp_metric_name in MAPPING.iteritems():
        metrics.append({
            "metric": cmp_metric_name % sample.get("dest-ip"),
            "value": sample.get(metric_name),
            "unit": "packets/s",
            "time": ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })

    return metrics
