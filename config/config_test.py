import json
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

data: dict

with open(ROOT_PATH / "config/config.json", "r") as config_file:
    data = json.load(config_file)

DB_NAME = 'heap_sort_test'

CONFIG_INIT = {
    'user': data['username_db'],
    'password': data['password_db'],
    'host': data['host']
}
CONFIG = {
    'user': data['username_db'],
    'password': data['password_db'],
    'host': data['host'],
    'database': 'heap_sort_test'
}
