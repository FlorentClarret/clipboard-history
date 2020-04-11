#! /usr/bin/env python3
# coding: utf-8

import os
import shutil
from datetime import datetime, timedelta

from clipboard_history.database import init, get_all, add, get_latest, delete_all

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestDatabase:

    def test_init(self):
        if os.path.exists(ROOT_DIR + 'data/database/tmp_database_init.txt'):
            os.remove(ROOT_DIR + 'data/database/tmp_database_init.txt')

        init(ROOT_DIR + 'data/database/tmp_database_init.txt')
        assert len(get_all()) == 0

    def test_get_all(self):
        init(ROOT_DIR + 'data/database/database_get_all.txt')
        result = get_all()

        assert len(result) == 2
        assert result[0].value == 'test2'
        assert result[0].date is not None
        assert result[1].value == 'test1'
        assert result[1].date is not None

    def test_add(self):
        if os.path.exists(ROOT_DIR + 'data/database/tmp_database_add.txt'):
            os.remove(ROOT_DIR + 'data/database/tmp_database_add.txt')

        init(ROOT_DIR + 'data/database/tmp_database_add.txt')
        assert len(get_all()) == 0

        now = datetime.now()
        add('tests', now, 1)

        objects = get_all()
        assert len(objects) == 1
        assert objects[0].value == 'tests'
        assert objects[0].date == now

    def test_add_max_element(self):
        if os.path.exists(ROOT_DIR + 'data/database/tmp_database_add.txt'):
            os.remove(ROOT_DIR + 'data/database/tmp_database_add.txt')

        init(ROOT_DIR + 'data/database/tmp_database_add.txt')
        assert len(get_all()) == 0

        now = datetime.now()
        add('tests1', now, 2)
        add('tests2', now + timedelta(days=1), 2)
        add('tests3', now + timedelta(days=2), 2)

        objects = get_all()
        assert len(objects) == 2
        assert objects[0].value == 'tests3'
        assert objects[0].date == now + timedelta(days=2)
        assert objects[1].value == 'tests2'
        assert objects[1].date == now + timedelta(days=1)

    def test_get_latest(self):
        shutil.copyfile(ROOT_DIR + 'data/database/database_get_latest.txt',
                        ROOT_DIR + 'data/database/tmp_database_get_latest.txt')
        init(ROOT_DIR + 'data/database/tmp_database_get_latest.txt')

        now = datetime.now()
        add('foo', now)
        result2 = get_latest()
        assert result2.value == 'foo'
        assert result2.date == now

        now = datetime.now()
        add('bar', now)
        result = get_latest()
        assert result.value == 'bar'
        assert result.date == now

    def test_delete_all(self):
        shutil.copyfile(ROOT_DIR + 'data/database/database_delete_all.txt',
                        ROOT_DIR + 'data/database/tmp_database_delete_all.txt')
        init(ROOT_DIR + 'data/database/tmp_database_delete_all.txt')

        assert len(get_all()) == 2
        delete_all()
        assert len(get_all()) == 0
