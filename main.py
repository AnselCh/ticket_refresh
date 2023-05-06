import time
import random
import json
from datetime import datetime

import requests

from func import AutoRun
from bs4 import BeautifulSoup

def get_config():
    import sys
    import os.path
    CWD = os.path.abspath(os.path.dirname(sys.executable))
    config_path = os.path.join(CWD, "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"Not getting config from {config_path}. "\
              "Assume running with source code. "\
              "Will be using ./config.json instead.")
        with open("config.json", "r") as f:
            return json.load(f)

def isNone(val):
    return val is None

def get_value_or_input(target, field, input_question):
    val = target.get(field)
    valid = False
    if type(val) is int:
        valid = True if val > 0 else False
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
    config = get_config()
    not_find_flag = True
    out_of_range = False
    target = config.get("target") or {}
    url = get_value_or_input(target, "url", '請輸入網址: ')
    area_id_start = get_value_or_input(target, "start", "搜尋起點: ")
    area_id_end = get_value_or_input(target, "end", "搜尋終點: ")

    ar = AutoRun(url, area_id_start, area_id_end, config)
    while not_find_flag:
        
        print('connecting...')
        try:
            response = requests.get(
                url, headers=ar.get_header())
        except:
            print('error url : {url}')
        not_find_flag, ts, out_of_range = ar.check_ticket_status(
            BeautifulSoup(response.text, "html.parser"))
        if out_of_range:
            print('請檢查輸入區間是否有誤')
            break

        print("The current time is", datetime.now().strftime("%H:%M:%S"))
        print(f''.join(ts))

        time.sleep(random.randint(1, 11))


if __name__ == '__main__':
    main()
