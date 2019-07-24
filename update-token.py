#!/usr/bin/env python
# -*-coding:utf-8 -*

import logging
import configparser
import click

from alkivi.logger import Logger

# Define the global logger
logger = Logger(min_log_level_to_mail=logging.WARNING,
                min_log_level_to_save=logging.DEBUG,
                min_log_level_to_print=logging.INFO,
                emails=['monitoring@alkivi.fr'])


@click.command()
@click.option('--dry', default=False, is_flag=True,
              help='Toggle DRY mode')
@click.option('--debug', default=False, is_flag=True,
              help='Toggle Debug mode')
def process(dry, debug):
    if debug:
        logger.set_min_level_to_print(logging.DEBUG)
        logger.set_min_level_to_save(logging.DEBUG)
        logger.set_min_level_to_mail(None)
        logger.set_min_level_to_syslog(None)
        logger.debug('debug activated')

    if dry:
        logger.set_min_level_to_print(logging.DEBUG)
        # Disable email warning
        logger.set_min_level_to_mail(None)
        logger.set_min_level_to_syslog(None)
        logger.info('DRY MODE activated')

    logger.info('Program start')

    config = configparser.ConfigParser()
    config.read('/tmp/todo')

    section = config.sections()[0]
    logger.new_loop_logger()
    for key in config[section]:
        logger.new_iteration(prefix=key)
        logger.debug('info')
    logger.del_loop_logger()





if __name__ == '__main__':
    try:
        process()
    except Exception as e:
        logger.exception(e)
