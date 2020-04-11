#! /usr/bin/env python3
# coding: utf-8

from datetime import datetime
from peewee import Model, DateTimeField, CharField, SqliteDatabase

_database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = _database


class CopyElement(BaseModel):
    date = DateTimeField()
    value = CharField()


def init(file):
    _database.init(file)
    _database.create_tables([CopyElement])


def add(data, date=datetime.now()):
    CopyElement(value=data, date=date).save()


def get_latest():
    return CopyElement.select().order_by(CopyElement.date.desc()).get()


def get_all():
    return list(CopyElement.select().order_by(CopyElement.date.asc()))


def delete_all():
    CopyElement.delete().execute()
