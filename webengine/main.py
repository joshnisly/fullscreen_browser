#!/usr/bin/env python3

import json
import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import config
import tabbed_browser


def main():
    root_url = config.Config().get_home_url() or 'https://www.google.com/'

    username, password = config.Config().get_auth()

    app = QtWidgets.QApplication(sys.argv)

    # Use a custom palette to make the highlighted text visible when searching.
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight,
                        palette.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText,
                        palette.color(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
    app.setPalette(palette)

    state_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../state.json')
    form_values = {}
    form_values_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../form_values.json')
    if os.path.exists(form_values_path):
        form_values = json.load(open(form_values_path))
    main_frame = tabbed_browser.MainFrame(state_path, root_url, username, password, form_values)
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
    # Make the monitor stay on.
    os.system('xset s off')
    os.system('xset -dpms')
    os.system('xset s noblank')

    main()
