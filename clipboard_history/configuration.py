#! /usr/bin/env python3
# coding: utf-8

""" This module deals with configuration files and default configuration """

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
    """ Class that holds all the configuration for the application """

    def __init__(self, path, app_dirs=AppDirs(APP_NAME, APP_AUTHOR)):
        self.app_dirs = app_dirs

        if not path and os.path.exists(
                self.app_dirs.user_config_dir + "/" + DEFAULT_CONFIGURATION_FILE):
            path = self.app_dirs.user_config_dir + "/" + DEFAULT_CONFIGURATION_FILE

        if path:
            with open(path, 'r') as file:
                self.config = json.load(file)
        else:
            self.config = None

    @property
    def database_location(self):
        """ Return the location of the database which store all the data """
        if self.config and self.config['database'] and self.config['database']['location']:
            return self.config['database']['location']

        if not os.path.exists(self.app_dirs.user_data_dir):
            os.mkdir(self.app_dirs.user_data_dir)

        return self.app_dirs.user_data_dir + "/" + DEFAULT_DATABASE_FILE

    @property
    def database_max_element(self):
        """ Return the maximum number of element to store in the database """
        if self.config and self.config['database'] and self.config['database']['max_element']:
            return int(self.config['database']['max_element'])

        return DEFAULT_DATABASE_MAX_ELEMENT

    @property
    def refresh_interval(self):
        """ Return the refresh interval to check to clipboard """
        if self.config and self.config['refresh_interval']:
            return float(self.config['refresh_interval'])

        return DEFAULT_REFRESH_INTERVAL
