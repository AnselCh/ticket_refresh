import requests
import time
from func import AutoRun
from bs4 import BeautifulSoup
from datetime import datetime
import random

def main():
    not_find_flag = True
    while not_find_flag:
        ar = AutoRun()
        print('connecting...')
        try:
            response = requests.get(
                "https://tixcraft.com/ticket/area/23_megaport/13729", headers=ar.get_header())
        except:
            print('error url : https://tixcraft.com/ticket/area/23_megaport/13729')
        not_find_flag,ts = ar.check_ticket_status(BeautifulSoup(response.text, "html.parser"))
        print("The current time is", datetime.now().strftime("%H:%M:%S"))
        print(f'\n'.join(ts))
        time.sleep(random.randint(3, 14))

if __name__ == '__main__':
    main()
