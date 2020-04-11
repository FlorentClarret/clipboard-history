#! /usr/bin/env python3
# coding: utf-8

import os
import shutil
from datetime import datetime

from clipboard_history.database import init, get_all, add, get_latest, delete_all

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestDatabase:

    def test_init(self):
        if os.path.exists(ROOT_DIR + 'data/tmp_database_init.txt'):
            os.remove(ROOT_DIR + 'data/tmp_database_init.txt')

        init(ROOT_DIR + 'data/tmp_database_init.txt')
        assert len(get_all()) == 0

    def test_get_all(self):
        init(ROOT_DIR + 'data/database_get_all.txt')
        result = get_all()

        assert len(result) == 2
        assert result[0].value == 'test1'
        assert result[0].date is not None
        assert result[1].value == 'test2'
        assert result[1].date is not None

    def test_add(self):
        if os.path.exists(ROOT_DIR + 'data/tmp_database_add.txt'):
            os.remove(ROOT_DIR + 'data/tmp_database_add.txt')

        init(ROOT_DIR + 'data/tmp_database_add.txt')
        assert len(get_all()) == 0

        now = datetime.now()
        add('tests', now)

        objects = get_all()
        assert len(objects) == 1
        assert objects[0].value == 'tests'
        assert objects[0].date == now

    def test_get_latest(self):
        shutil.copyfile(ROOT_DIR + 'data/database_get_latest.txt',
                        ROOT_DIR + 'data/tmp_database_get_latest.txt')
        init(ROOT_DIR + 'data/tmp_database_get_latest.txt')
        now = datetime.now()

        result = get_latest()
        assert result.value == 'test2'
        assert result.date is not None

        add('foo', now)
        result = get_latest()
        assert result.value == 'foo'
        assert result.date == now

    def test_delete_all(self):
        shutil.copyfile(ROOT_DIR + 'data/database_delete_all.txt',
                        ROOT_DIR + 'data/tmp_database_delete_all.txt')
        init(ROOT_DIR + 'data/tmp_database_delete_all.txt')

        assert len(get_all()) == 2
        delete_all()
        assert len(get_all()) == 0