# Nflex Training demo script
from viptela import Viptela

VIPTELA_USERNAME = 'matthew'
VIPTELA_PSWD = 'R0ug30n3!'
VIPTELA_SERVER = '54.251.162.192'

def get_resources(event, context):
    vip_cli = Viptela(VIPTELA_USERNAME, VIPTELA_PSWD, VIPTELA_SERVER) 
    devices = vip_cli.get_devices()
    print 'devices - {}'.format(devices)
