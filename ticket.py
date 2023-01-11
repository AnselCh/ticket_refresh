import requests,time,sys,random
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets
from datetime import datetime


def TS1():
    if T1.text[-1:] != 't':
        return T1.text


def TS2():
    if T2.text[-1:] != 't':
        return T2.text


def TS3():
    if T3.text[-1:] != 't':
        return T3.text


def TS4():
    if T4.text[-1:] != 't':
        return T4.text


def win():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowTitle('ticket')
    Form.resize(100, 20)
    label = QtWidgets.QLabel(Form)   # 在 Form 裡加入標籤
    label.setText('搶票加油!')
    mbox = QtWidgets.QMessageBox(Form)       # 加入對話視窗
    mbox.information(
        Form, 'info', f'{T1.text}\n{T2.text}\n{T3.text}\n{T4.text}')
    Form.show()
    sys.exit(app.exec_())


headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
           "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            ]
#隨機選擇headers
user_agent = random.choice(headerlist)
headers = {'User-Agent': user_agent}
while True:
    print('connecting...')
    try:
        response = requests.get(
            "https://tixcraft.com/ticket/area/23_megaport/13729", headers=headers)
    except:
        print('error url : https://tixcraft.com/ticket/area/23_megaport/13729')
    soup = BeautifulSoup(response.text, "html.parser")
    ticket_status = soup.find('div', class_='zone area-list')
    T1 = ticket_status.find('ul', id='group_20944')
    T2 = ticket_status.find('ul', id='group_20945')
    T3 = ticket_status.find('ul', id='group_20946')
    T4 = ticket_status.find('ul', id='group_20947')
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M:%S")
    print("The current time is", currentTime)
    if TS1() != None or TS2() != None or TS3() != None or TS4() != None:
        win()
        break
    print(f'{T1.text}\n{T2.text}\n{T3.text}\n{T4.text}')
    time.sleep(2)
    time.sleep(random.randint(1,11))
