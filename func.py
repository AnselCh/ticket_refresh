import sys
import random
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *

class AutoRun:
    def __init__(self) -> None:
        self.header=self.read_header()

    def read_header(self)->list:
        with open('headerlist.txt','r') as f:
            return f.read().splitlines()

    def get_header(self)->dict:
        return {'User-Agent':random.choice(self.header)}

    def has_ticket_alarm(self,ts:list)->None:
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        Form.setWindowFlags(Qt.WindowStaysOnTopHint)
        Form.setWindowTitle('ticket')
        Form.resize(500, 180)
        label = QtWidgets.QLabel(Form)   # 在 Form 裡加入標籤
        label.setText(f'\n'.join(ts))
        font = QtGui.QFont()                       # 加入文字設定
        font.setPointSize(20)                      # 文字大小
        font.setBold(True)                         # 粗體
        label.setFont(font)
        Form.show()
        sys.exit(app.exec_())

    def check_ticket_status(self,soup:BeautifulSoup):
        ticket_status = soup.find('div', class_='zone area-list')
        ticket_status_list=[]
        for i in range(20944,20948):#area id range
            ticket_status_list.append(ts:=ticket_status.find('ul',id='group_{}'.format(i)).text)
            find_flag = False if 'out' in ts else True
        if find_flag:
            self.has_ticket_alarm(ticket_status_list)
            return False,ticket_status_list
        else:
            return True,ticket_status_list


    
    