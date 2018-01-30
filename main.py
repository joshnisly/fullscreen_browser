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

import tabbed_browser

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


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Use a custom palette to make the highlighted text visible when searching.
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight,
                        palette.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText,
                        palette.color(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
    app.setPalette(palette)

    state_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state.json')
    main_frame = tabbed_browser.MainFrame(state_path, ROOT_URL, USERNAME, PASSWORD)
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
