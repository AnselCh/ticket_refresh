import requests
import time
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets
import sys


def TS1():
    if T1.text[-1:] != 't':
        return T1.text


def TS2():
    if T2.text[-1:] != 't':
        return T1.text


def TS3():
    if T3.text[-1:] != 't':
        return T1.text


def TS4():
    if T4.text[-1:] != 't':
        return T1.text


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


while True:
    response = requests.get(
        "https://tixcraft.com/ticket/area/23_megaport/13729")

    soup = BeautifulSoup(response.text, "html.parser")
    ticket_status = soup.find('div', class_='zone area-list')
    T1 = ticket_status.find('ul', id='group_20944')
    T2 = ticket_status.find('ul', id='group_20945')
    T3 = ticket_status.find('ul', id='group_20946')
    T4 = ticket_status.find('ul', id='group_20947')

    if TS1() != None:
        win()
    if TS2() != None:
        print(T2.text)
    if TS3() != None:
        print(T3.text)
    if TS4() != None:
        print(T4.text)

    time.sleep(10)
