import logging
import random
import string
from datetime import datetime
from datetime import timedelta

from faker import Faker

# create and initialize a faker generator. Ireland localisation arg provided
fake_generator = Faker('en_IE')

current_dt_obj = datetime.now()
# Can use 'current_dt_obj' to get other date parts. E.g. 'current_dt_obj.year'
current_date_str = current_dt_obj.strftime('%d-%m-%Y')
current_time_str = current_dt_obj.strftime('%H:%M:%S')

# Set up a specific logger with our desired output level"""
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)


def gen_fake_string_data(row):

    fake_string_data = ''

    if row['col_name'].upper() == 'FIRST_NAME':
        fake_string_data = fake_generator.first_name()

    elif row['data_type'].startswith('VARCHAR'):
        varchar_length = row['data_type'].split('(')[1].split(')')[0]

        fake_string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(int(varchar_length)))

    return fake_string_data


def gen_fake_numeric_data(row):

    fake_numeric_data = ''

    if row['data_type'].startswith('NUMBER'):

        split_str = row['data_type'].split('(')[1].split(',')
        precision = split_str[0]

        logger.debug(f'precision = {precision}')
        # scale = split_str[1].split(")")[0]

        # print(precision.MAX_PREC)

        # generate random number to (max) precision
        # fake_numeric_data = random.randint(1, 10**int(precision))

        # generating data to 38 precision produces too high numbers. Just limit to 100
        fake_numeric_data = random.randint(1, 100)

    return fake_numeric_data


def gen_fake_date_time_data(row):

    # TODO: multiple checks, e.g.: date vs datetime vs time?
    fake_date_time_data = ''

    fake_date_time_data = f"to_date('{fake_generator.date_between(current_dt_obj - timedelta(days=5), current_dt_obj)}')"

    return fake_date_time_data
