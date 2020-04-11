#! /usr/bin/env python3
# coding: utf-8

import argparse
import logging
import uuid
from time import sleep

import pyperclip

from clipboard_history import database

LOG_FORMAT = '%(asctime)-15s %(message)s'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="""The file to store the data""",
                        default="/tmp/{}.sql".format(str(uuid.uuid4())).replace('-', ''))
    return parser.parse_args()


def main():
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    logger = logging.getLogger('clipboard-history')

    args = parse_arguments()

    database.init(args.file)

    last_copy = pyperclip.paste()

    while True:
        try:
            sleep(0.1)
            new_copy = pyperclip.paste()

            if new_copy != last_copy:
                last_copy = new_copy
                database.add(new_copy)
                logger.info('Copying \'%s\'', new_copy)
        except KeyboardInterrupt:
            logger.info('Stopping')
            exit()


if __name__ == '__main__':
    main()
