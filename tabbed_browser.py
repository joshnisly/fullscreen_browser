
import json
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtNetwork

import web_tab


class MainFrame(QtWidgets.QMainWindow):
    def __init__(self, state_path, initial_url, username, password):
        QtWidgets.QMainWindow.__init__(self, None)
        self._state_path = state_path
        self._initial_url = initial_url
        self._username = username
        self._password = password

        self.tabs = QtWidgets.QTabWidget(self,
                                         tabsClosable=True,
                                         movable=True,
                                         elideMode=QtCore.Qt.ElideRight,
                                         tabCloseRequested=lambda idx: self.tabs.removeTab(idx))
        self.tabs.setTabBarAutoHide(True)
        self.setCentralWidget(self.tabs)
        self.tabWidgets = []

        self._cookies = QtNetwork.QNetworkCookieJar()
        self._load_cookies()

        self.add_tab(QtCore.QUrl(self._initial_url))

    def get_cookies(self):
        return self._cookies

    def add_tab(self, url=None):
        print('add_tab', url)
        url = url or ''
        url = QtCore.QUrl(url)
        new_tab = web_tab.Tab(url, self, self._username, self._password)
        self.tabs.setCurrentIndex(self.tabs.addTab(new_tab, ''))
        return self.tabs.currentWidget()

    def closeEvent(self, event):
        cookies = [str(c.toRawForm()) for c in self._cookies.allCookies()]
        self._set_state_value('cookies', cookies)
        return QtWidgets.QMainWindow.closeEvent(self, event)

    def _load_cookies(self):
        cookies = []
        for cookie in self._get_state_value('cookies', []):
            cookie_bytes = QtCore.QByteArray(cookie.encode('utf-8'))
            cookies.append(QtNetwork.QNetworkCookie.parseCookies(cookie_bytes)[0])

        self._cookies.setAllCookies(cookies)

    def _get_state_value(self, key, default=None):
        all_settings = self._internal_load_state()
        return all_settings.get(key, default)

    def _set_state_value(self, key, value):
        all_settings = self._internal_load_state()

        all_settings[key] = value
        with open(self._state_path, 'w') as output:
            output.write(json.dumps(all_settings))

    def _internal_load_state(self):
        try:
            return json.loads(open(self._state_path).read())
        except Exception:
            return {}
