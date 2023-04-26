import requests
import time
from func import AutoRun
from bs4 import BeautifulSoup
from datetime import datetime
import random


def main():
    not_find_flag = True
    out_of_range = False
    url = str(input('請輸入網址:'))
    area_id_start = int(input("搜尋起點:"))
    area_id_end = int(input("搜尋終點:"))

    while not_find_flag:
        ar = AutoRun(area_id_start, area_id_end)
        print('connecting...')
        try:
            response = requests.get(
                url, headers=ar.get_header())
        except:
            print('error url : {url}')
        not_find_flag, ts , out_of_range = ar.check_ticket_status(
            BeautifulSoup(response.text, "html.parser"))
        if out_of_range:
            print('請檢查輸入區間是否有誤')
            break
        print("The current time is", datetime.now().strftime("%H:%M:%S"))
        print(f'\n'.join(ts))

        time.sleep(random.randint(1, 11))

            

if __name__ == '__main__':
    main()
