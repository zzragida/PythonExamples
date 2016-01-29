YAML_CONFIG = './settings.yaml'

import yaml

stream = file(YAML_CONFIG, 'r')
config = yaml.load(stream)

DUMP_PACKET = config['network']['dump_packet']
DUMP_TRAFFIC = config['network']['dump_traffic']

SQLRELAY = config['sqlrelays']
