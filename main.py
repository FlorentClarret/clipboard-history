#! /usr/bin/env python3
# coding: utf-8

import argparse
import logging
from time import sleep

import pyperclip

from clipboard_history import database
from clipboard_history.configuration import Configuration

LOG_FORMAT = '%(asctime)-15s %(message)s'

DEFAULT_DATABASE_FILE = "database.sqlite"
DEFAULT_CONFIGURATION_FILE = "clipboard-history.conf"


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="""The configuration file""", default=None)
    return parser.parse_args()


def main():
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    logger = logging.getLogger('clipboard-history')

    args = parse_arguments()
    config = Configuration(args.config)

    logger.info("Database location : %s", config.database_location)
    database.init(config.database_location)

    last_copy = pyperclip.paste()

    while True:
        try:
            sleep(config.refresh_interval)
            new_copy = pyperclip.paste()

            if new_copy != last_copy:
                last_copy = new_copy
                database.add(new_copy, config.database_max_element)
                logger.info('Copying \'%s\'', new_copy)
        except KeyboardInterrupt:
            logger.info('Stopping')
            exit()


if __name__ == '__main__':
    main()
