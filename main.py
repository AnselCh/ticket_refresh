import time
import random
import json
from datetime import datetime
import sys
import os.path

import requests
from bs4 import BeautifulSoup

from auto_run import AutoRun
import config as cfg
import requests_operations as req

def get_config_path():
    CWD = os.path.abspath(os.path.dirname(sys.executable))
    config_path = os.path.join(CWD, "config.json")
    if "venv" in config_path:  # assume running in devel mode
        print("=== RUNNING IN DEVELOP MODE ===")
        config_path = "config.json"
    return config_path

def get_config(config_path):
    if not os.path.isfile(config_path):
        config = cfg.create_config_content()
    else:
        with open(config_path, "r") as f:
            return json.load(f)
    return config

def save_config(config: dict, config_path):
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=4))

def get_value_or_input(target, field, input_question):
    val = target.get(field)
    valid = False
    if type(val) is int:
        valid = True if val >= 0 else False
    if type(val) is str:
        valid = True if val else False
    if valid:
        return val

    answer = input(input_question)
    try:
        return int(answer)
    except ValueError:
        return answer

def main():
    config_path = get_config_path()
    config = get_config(config_path)
    not_find_flag = True
    out_of_range = False

    config = cfg.validate_config(config)
    save_config(config, config_path)
    target = config.get("target")
    url = target.get("url")

    cfg.pretty_print_config(config)

    ar = AutoRun(config)
    while not_find_flag:

        print('connecting...')
        response = req.request(url, headers=ar.get_header())

        not_find_flag, ts, out_of_range = ar.check_ticket_status(response)
        if out_of_range:
            print('請檢查輸入區間是否有誤')
            break

        print("The current time is", datetime.now().strftime("%H:%M:%S"))
        print(f''.join(ts))

        time.sleep(random.randint(1, 11))


if __name__ == '__main__':
    main()
