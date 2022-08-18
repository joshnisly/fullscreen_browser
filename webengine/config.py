#!/usr/bin/env python3

import configparser
import os


class Config(object):
    def __init__(self):
        self._path = os.path.join(os.environ['HOME'], '.fullscreen_browser', 'config.ini')
        self._parser = configparser.ConfigParser()
        if os.path.exists(self._path):
            self._parser.read(self._path)

    def get_cache_path(self):
        path = self._parser.get('App', 'CachePath', fallback=os.path.join(os.environ['HOME'], '.fullscreen_browser', 'cache'))
        os.makedirs(path, exist_ok=True)
        return path

    def get_log_path(self):
        return self._parser.get('App', 'DebugLogPath',
                                fallback=os.path.join(os.environ['HOME'], '.fullscreen_browser', 'debug.log'))

    def get_home_url(self):
        return self._parser.get('App', 'HomeUrl', fallback='https://www.google.com/').rstrip('/') + '/'

    def get_auth(self):
        if not self._parser.has_option('Auth', 'Username'):
            return None, None
        return self._parser.get('Auth', 'Username'), self._parser.get('Auth', 'Password')
