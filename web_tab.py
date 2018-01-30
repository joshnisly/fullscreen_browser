#!/usr/bin/python

import json
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


class Tab(QtWebKitWidgets.QWebView):
    def __init__(self, url, container):
        QtWebKitWidgets.QWebView.__init__(self)
        self._container = container
        self.setPage(_WebPage())
        self.page().networkAccessManager().setCookieJar(container.get_cookies())
        self.page().setForwardUnsupportedContent(True)

        self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, True)

        self.load(url)

    def createWindow(self, windowType):
        QtWebKitWidgets.QWebView.createWindow(self, windowType)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, True)
        return self._container.add_tab()
