import sys
import requests
from typing import Dict
from bs4 import BeautifulSoup
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import *

import html_parser as parser
from requests_operations import send_line_msg
try:
    from fake_useragent import UserAgent
except:
    pass

class AutoRun:

    def __init__(
            self,
            config: dict) -> None:
        self.header = self.read_header()
        self.target = config.get("target")
        self.url = self.target.get("url")
        self.group_ids = self.target.get("group_ids")
        self.title = None
        self.notification_type = config.get("notification_type") or {}
        self.token = config.get("token") or {}

    def read_header(self) -> str:
        try:
            ua = UserAgent(use_external_data=True)
            user_agent = ua.random
            return user_agent
        except:
            pass

    def get_header(self) -> dict:
        try:
            return {'User-Agent': self.header}
        except: pass

    def __del__(self) -> None:
        if self.notification_type.get("line"):
            send_line_msg(
                self.token["line"],
                self.title,
                "結束監看餘票。\n",
                self.url)

    def has_ticket_alarm(self, ts:list) -> None:
        if self.notification_type.get("line"):
            self._has_ticket_alarm_line(ts)
        if self.notification_type.get("window"):
            self._has_ticket_alarm_qt(ts)

    def _has_ticket_alarm_line(self, ts:list=[], msg_overwrite="") -> None:
        remain_ticket = []
        for t in ts:
            if 'remain' in t:
                remain_ticket.append(f''.join(t))
        msg_body = "".join(remain_ticket)
        send_line_msg(self.token["line"], self.title, msg_body, self.url)

    def _has_ticket_alarm_qt(self, ts: list) -> None:
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
        if self.title is None:
            self.title = parser.parse_title(soup)
            send_line_msg(
                self.token["line"],
                self.title,
                "開始監看餘票：）\n",
                self.url)
        ticket_status = soup.find('div', class_='zone area-list')
        ticket_status_list = []
        find_flag = False
        # print(ticket_status)
        for group_id in self.group_ids:
            try:
                group_ul = ticket_status.find('ul', id=group_id)
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

if __name__ == '__main__':
    # url = "https://tixcraft.com/ticket/area/23_more2come/14445"
    url = "https://tixcraft.com/ticket/area/23_reneliu/14411"
    ar = AutoRun(url, 0, 0, {})
    response = requests.get(
        url, headers=ar.get_header())
    ar.parse_zone_info(BeautifulSoup(response.text, "html.parser"))