#! /usr/bin/env python3
# coding: utf-8

import json
import os

from appdirs import AppDirs

APP_NAME = 'clipboard_history'
APP_AUTHOR = 'florent_clarret'

DEFAULT_DATABASE_FILE = "database.sqlite"
DEFAULT_DATABASE_MAX_ELEMENT = 50
DEFAULT_REFRESH_INTERVAL = 0.1

DEFAULT_CONFIGURATION_FILE = "clipboard-history.conf"


class Configuration:
    def __init__(self, path):
        if not path:
            app_dirs = AppDirs(APP_NAME, APP_AUTHOR)

            if os.path.exists(app_dirs.user_config_dir + "/" + DEFAULT_CONFIGURATION_FILE):
                path = app_dirs.user_config_dir + "/" + DEFAULT_CONFIGURATION_FILE

        if path:
            with open(path, 'r') as file:
                self.config = json.load(file)
        else:
            self.config = None

    @property
    def database_location(self):
        if self.config and self.config['database'] and self.config['database']['location']:
            return self.config['database']['location']

        app_dirs = AppDirs(APP_NAME, APP_AUTHOR)

        if not os.path.exists(app_dirs.user_data_dir):
            os.mkdir(app_dirs.user_data_dir)

        return app_dirs.user_data_dir + "/" + DEFAULT_DATABASE_FILE

    @property
    def database_max_element(self):
        if self.config and self.config['database'] and self.config['database']['max_element']:
            return int(self.config['database']['max_element'])

        return DEFAULT_DATABASE_MAX_ELEMENT

    @property
    def refresh_interval(self):
        if self.config and self.config['refresh_interval']:
            return float(self.config['refresh_interval'])

        return DEFAULT_REFRESH_INTERVAL
