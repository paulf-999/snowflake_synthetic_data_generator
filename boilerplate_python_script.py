#!/usr/bin/env python3
"""
Python Version  : 3.8
# TODO: change these
* Name          : boilerplate_python_script.py
* Description   : Boilerplate python script
* Created       : 26-02-2021
* Usage         : python3 boilerplate_python_script.py
"""

__author__ = 'Paul Fry'
__version__ = '1.0'

import os
from datetime import datetime
import logging
import yaml

working_dir = os.getcwd()
current_dt_obj = datetime.now()
# Can use 'current_dt_obj' to get other date parts. E.g. 'current_dt_obj.year'
current_date_str = current_dt_obj.strftime('%d-%m-%Y')
current_time_str = current_dt_obj.strftime('%H:%M:%S')


def get_logger():
    """Set up a specific logger with our desired output level"""
    logging.basicConfig(format='%(message)s')
    logger = logging.getLogger('application_logger')
    logger.setLevel(logging.INFO)

    return logger


def read_ip():
    """Read input from config file"""

    logger = get_logger()

    with open('ip/config.yaml') as ip_yml:
        data = yaml.safe_load(ip_yml)

    env = data['general_params']['env']
    logger.info(f'env = {env}')

    return


def function_template():
    """Description here"""
    logger = get_logger()

    logger.info('Hello, world!')

    return


def main():
    """Main entry point of the app"""
    logger = get_logger()
    logger.info('example')

    # program logic here
    function_template()

    return


if __name__ == '__main__':
    """This is executed when run from the command line"""

    main()
