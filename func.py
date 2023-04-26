import sys
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from fake_useragent import UserAgent


class AutoRun:

    def __init__(self, area_id_start, area_id_end) -> None:
        self.header = self.read_header()
        self.area_id_start = area_id_start
        self.area_id_end = area_id_end

    def read_header(self) -> str:
        ua = UserAgent()
        user_agent = ua.random
        return user_agent

    def get_header(self) -> dict:
        return {'User-Agent': self.header}

    def has_ticket_alarm(self, ts: list) -> None:
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

    def check_ticket_status(self, soup: BeautifulSoup):
        ticket_status = soup.find('div', class_='zone area-list')
        ticket_status_list = []
        # print(ticket_status)
        for i in range(self.area_id_start, self.area_id_end + 1):  # area id range
            # ticket_status_list.append(ts := ticket_status.find(
            #     'ul', id='group_{}'.format(i)).text)
            group_ul = ticket_status.find('ul', id=f'group_{i}')
            if group_ul is None:
                continue
            lis = group_ul.find_all('li')
            for li in lis:
                print(li.text)
                ticket_status_list.append(li.text + '\n')

                find_flag = False if 'out' in li else True
        if find_flag:
            self.has_ticket_alarm(ticket_status_list)
            return False, ticket_status_list
        else:
            return True, ticket_status_list
