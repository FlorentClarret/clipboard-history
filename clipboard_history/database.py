#! /usr/bin/env python3
# coding: utf-8

""" This module allow to interact with the database """

from datetime import datetime
from peewee import Model, DateTimeField, CharField, SqliteDatabase

_DATABASE = SqliteDatabase(None)


class BaseModel(Model):
    """ Super class for all the entity stored in the database """
    class Meta:
        # pylint: disable=R0903
        """ Specify the database """
        database = _DATABASE


class CopyElement(BaseModel):
    """ Represent a copied element"""
    date = DateTimeField()
    value = CharField()


def init(file):
    """ Initialize the database using the given file """
    _DATABASE.init(file)
    _DATABASE.create_tables([CopyElement])


def add(data, date=datetime.now(), max_element=50):
    """ And a copied element to the database """
    if CopyElement.select().count() >= max_element:
        CopyElement.delete_instance(CopyElement.select().order_by(CopyElement.date.asc()).get())
    CopyElement(value=data, date=date).save()


def get_latest():
    """ Return the latest element stored in the database """
    return CopyElement.select().order_by(CopyElement.date.desc()).get()


def get_all():
    """ Return all the copied elements stored in the database as a list """
    return list(CopyElement.select().order_by(CopyElement.date.desc()))


def delete_all():
    """ Delete all the elements from the database """
    CopyElement.delete().execute(_DATABASE)
