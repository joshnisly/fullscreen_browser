
import sys
import os
sys.path.insert(0, os.path.join(os.environ['HOME'], '.local', 'lib', 'python3.8', 'site-packages'))

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets


class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent, username, password, form_values):
        super().__init__(parent)
        self._username = username
        self._password = password
        self._form_values = form_values

        self.authenticationRequired.connect(self._get_auth)

    def _get_auth(self, url, auth):
        auth.setUser(self._username)
        auth.setPassword(self._password)
        return True


class MainFrame(QtWidgets.QMainWindow):
    def __init__(self, state_path, initial_url, username, password, form_values):
        QtWidgets.QMainWindow.__init__(self, None)
        self._state_path = state_path
        self._initial_url = initial_url
        self._username = username
        self._password = password
        self._form_values = form_values

        QtWebEngineWidgets.QWebEngineProfile.defaultProfile().setHttpCacheType(QtWebEngineWidgets.QWebEngineProfile.MemoryHttpCache)

        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.page = WebPage(None, username, password, form_values)
        self.view.setPage(self.page)

        if '--debug' in sys.argv:
            layout = QtWidgets.QGridLayout()
            # noinspection PyArgumentList
            layout.addWidget(self.view, 0, 0)

            self.tools_view = QtWebEngineWidgets.QWebEngineView(self)
            self.tools_page = QtWebEngineWidgets.QWebEnginePage()
            self.tools_view.setPage(self.tools_page)
            self.page.setDevToolsPage(self.tools_page)
            layout.addWidget(self.tools_view, 1, 0)

            frame = QtWidgets.QFrame()
            frame.setLayout(layout)
            self.setCentralWidget(frame)
        else:
            self.setCentralWidget(self.view)

        self.page.load(QtCore.QUrl(initial_url))


