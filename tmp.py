import requests
import time
from func import AutoRun
from bs4 import BeautifulSoup
from datetime import datetime
import random
from fake_useragent import UserAgent


url = "https://www.uniair.com.tw/rwd/B2C/booking/ubk_select-itinerary.aspx"

ua = UserAgent()
user_agent = ua.random

try:
    response = requests.get(
        url, headers=user_agent)
    print(response)
except:
    print('error url')
