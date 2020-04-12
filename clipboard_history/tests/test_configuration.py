#! /usr/bin/env python3
# coding: utf-8

import os

from clipboard_history.configuration import Configuration

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestConfiguration:
    def test_database_location(self):
        config = Configuration(ROOT_DIR + 'data/conf/custom.conf')
        assert config.database_location == 'custom_database.sqlite'

    def test_max_element(self):
        config = Configuration(ROOT_DIR + 'data/conf/custom.conf')
        assert config.database_max_element == 30

    def test_refresh_interval(self):
        config = Configuration(ROOT_DIR + 'data/conf/custom.conf')
        assert config.refresh_interval == 0.5

    def test_database_location_default(self):
        config = Configuration(None, self.mock_app_dirs())
        assert config.database_location == ROOT_DIR + 'data/tmp/data/database.sqlite'

    def test_max_element_default(self):
        config = Configuration(None, self.mock_app_dirs())
        assert config.database_max_element == 50

    def test_refresh_interval_default(self):
        config = Configuration(None, self.mock_app_dirs())
        assert config.refresh_interval == 0.1

    @staticmethod
    def mock_app_dirs():
        os.makedirs(ROOT_DIR + 'data/tmp/config', exist_ok=True)
        os.makedirs(ROOT_DIR + 'data/tmp/data', exist_ok=True)

        return type('obj',
                    (object,),
                    {
                        'user_config_dir': ROOT_DIR + 'data/tmp/config',
                        'user_data_dir': ROOT_DIR + 'data/tmp/data'
                    }
                    )
