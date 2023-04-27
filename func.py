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

        # 設置窗口大小
        Form.resize(500, 400)
        scroll_area = QtWidgets.QScrollArea(Form)
        scroll_area.setGeometry(0, 0, Form.width(), Form.height())  # 設置滾動區域的大小
        scroll_area.setWidgetResizable(True)
        remain_ticket = []
        label = QtWidgets.QLabel(scroll_area)
        for t in ts:
            if 'remain' in t:
                remain_ticket.append(
                    '<font color=\"#ff6666\">'+f''.join(t)+'</font><br>')

        label.setText(f''.join(remain_ticket))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        label.setFont(font)

        scroll_area.setWidget(label)
        scroll_area.show()
        Form.show()
        sys.exit(app.exec_())

    def check_ticket_status(self, soup: BeautifulSoup):
        ticket_status = soup.find('div', class_='zone area-list')
        ticket_status_list = []
        find_flag = False
        # print(ticket_status)
        for i in range(self.area_id_start, self.area_id_end + 1):  # area id range

            try:
                group_ul = ticket_status.find('ul', id=f'group_{i}')
                lis = group_ul.find_all('li')
                for li in lis:
                    # print(li.text)
                    ticket_status_list.append(li.text + '\n')
                    if 'out' not in li.text:
                        find_flag = True
            except:
                return True, ticket_status_list, True  # 當找不到tag返回out_of_range==True
        if find_flag:
            self.has_ticket_alarm(ticket_status_list)
            return False, ticket_status_list, False
        else:
            return True, ticket_status_list, False
