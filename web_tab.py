#!/usr/bin/python

import json
from PyQt5 import QtNetwork
from PyQt5 import QtWebKit
from PyQt5 import QtWebKitWidgets
import sys


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


class _LoggingManager(QtNetwork.QNetworkAccessManager):
    def __init__(self):
        QtNetwork.QNetworkAccessManager.__init__(self)
        # add event listener on "load finished" event
        self.finished.connect(self._finished)

    def _finished(self, reply):
        """Update table with headers, status code and url.
        """
        headers = reply.rawHeaderPairs()
        headers = {str(k):str(v) for k,v in headers}
        print headers
        print reply.url().toString()
        status = reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        print status


class Tab(QtWebKitWidgets.QWebView):
    def __init__(self, url, container, username, password, form_values):
        QtWebKitWidgets.QWebView.__init__(self)
        self._container = container
        self._username = username
        self._password = password
        self._form_values = form_values
        self.setPage(_WebPage())
        if False: # Enable to see request logging.
            self.page().setNetworkAccessManager(_LoggingManager())
        self.page().networkAccessManager().setCookieJar(container.get_cookies())
        self.page().setForwardUnsupportedContent(True)

        self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, True)

        self.page().networkAccessManager().authenticationRequired.connect(self._on_auth)
        self.page().networkAccessManager().sslErrors.connect(self._on_auth)
        self.page().windowCloseRequested.connect(self._on_close)

        self.loadFinished.connect(self._loadFinished)

        self.load(url)

    def createWindow(self, windowType):
        QtWebKitWidgets.QWebView.createWindow(self, windowType)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, True)
        return self._container.add_tab()

    def _on_close(self):
        self._container.tabs.removeTab(self._container.tabs.currentIndex())

    def _loadFinished(self, ok):
        frame = self.page().currentFrame()
        for name, value in self._form_values['inputs'].items():
            elems = frame.findAllElements('input[name="%s"]' % name)
            for elem in elems:
                elem.setAttribute('value', value)

        for button in self._form_values['buttons']:
            elems = frame.findAllElements(button)
            for elem in elems:
                elem.evaluateJavaScript("this.click()")

    def _on_ssl_errors(self, reply, errors):
        reply.ignoreSslErrors()

    def _on_auth(self, reply, authenticator):
        authenticator.setUser(self._username)
        authenticator.setPassword(self._password)
