#!/usr/bin/python

import sys

import ConfigParser
import json
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtNetwork
from PyQt5 import QtWebKit
from PyQt5 import QtWebKitWidgets


ROOT_URL = 'https://www.google.com/'

settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')

config = ConfigParser.ConfigParser()
config.read(settings_path)
if config.has_option('Settings', 'Url'):
    ROOT_URL = config.get('Settings', 'Url')

USERNAME = ''
PASSWORD = ''
if config.has_option('Auth', 'Username'):
    USERNAME = config.get('Auth', 'Username')
    PASSWORD = config.get('Auth', 'Password')


class _WebPage(QtWebKitWidgets.QWebPage):
    """
    QWebPage that prints Javascript errors to stderr.
    """
    def javaScriptConsoleMessage(self, message, lineNumber, sourceID):
        msg = 'Javascript error at line number %d\n%s\nSource ID: %s\n' % (
                lineNumber,
                message,
                sourceID
            )
        sys.stderr.write(msg)
        sys.stderr.flush()
        QtGui.QMessageBox.critical(self.view(), self.tr("JavaScript Error"), msg)

    def eval_if_loaded(self, function_name, *args):
        """ Evalutes a JavaScript function. Returns true if it was defined;
            otherwise, returns false.
        """
        script = """
            (function()
            {
                var fn = window.%(function_name)s;
                if (typeof fn !== 'undefined')
                {
                    fn(%(args)s);
                    return true;
                }
                else
                    return false;
            })()
        """ % {
                'function_name': function_name,
                'args': ', '.join([json.dumps(arg) for arg in args])
            }

        qresult = self.mainFrame().evaluateJavaScript(script)
        return qresult.toBool()


class MainFrame(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.setWindowTitle(self.tr('Browser'))

        # Create main window and setup events
        self.view = QtWebKitWidgets.QWebView()

        self.setCentralWidget(self.view)

        self.view.setPage(_WebPage())

        # Disable and hide various actions. This needs to happen after we call setPage.
        for action in (QtWebKitWidgets.QWebPage.DownloadLinkToDisk,
                        QtWebKitWidgets.QWebPage.OpenLinkInNewWindow,
                        QtWebKitWidgets.QWebPage.OpenFrameInNewWindow,
                        QtWebKitWidgets.QWebPage.DownloadImageToDisk,
                        QtWebKitWidgets.QWebPage.OpenImageInNewWindow):
            self.view.pageAction(action).setEnabled(False)
            self.view.pageAction(action).setVisible(False)

        self.manager = QtNetwork.QNetworkAccessManager()
        #self.connect(self.manager, QtCore.SIGNAL('authenticationRequired(QNetworkReply*, QAuthenticator*)'),
        #             self._on_auth)
        #self.connect(self.manager, QtCore.SIGNAL('sslErrors(QNetworkReply *, QList<QSslError>)'),
        #             self._on_ssl_errors)

        self.view.page().setNetworkAccessManager(self.manager)

        # Set the home page
        self.view.setUrl(QtCore.QUrl(ROOT_URL))

    def _on_ssl_errors(self, reply, errors):
        reply.ignoreSslErrors()

    def _on_auth(self, reply, authenticator):
        authenticator.setUser(USERNAME)
        authenticator.setPassword(PASSWORD)


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Use a custom palette to make the highlighted text visible when searching.
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight,
                        palette.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText,
                        palette.color(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
    app.setPalette(palette)

    main_frame = MainFrame(None)
    if '--restored' in sys.argv:
        main_frame.show()
    else:
        main_frame.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        main_frame.showFullScreen()
        main_frame.setFocus()
        main_frame.activateWindow()
        main_frame.raise_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
