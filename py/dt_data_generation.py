import logging
import random
import string
from datetime import date
from datetime import datetime
from datetime import timedelta

from faker import Faker

current_dt_obj = datetime.now()

# create and initialize a faker generator. Ireland localisation arg provided
fake_generator = Faker('en_IE')

# Set up a specific logger with our desired output level"""
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)


def gen_fake_string_data(row):

    fake_string_data = ''

    if row['col_name'].upper() == 'FIRST_NAME':
        fake_string_data = fake_generator.first_name()
    # to facilitate table joins, limit IDs to a range of 10 values
    elif 'ID' in row['col_name'].upper():
        fake_string_data = str(random.randint(1, 10))
    # in case a date field is accidently captured as a string, include data generation for it here
    elif 'DATE' in row['col_name'].upper():
        fake_string_data = f"to_date('{fake_generator.date_between(current_dt_obj - timedelta(days=5), current_dt_obj)}')"

    elif row['data_type'].startswith('VARCHAR'):
        # generating a string to max length produces too long strings. Limit to 20 and uncomment the line below if otherwise wanted.
        # varchar_length = row['data_type'].split('(')[1].split(')')[0]

        fake_string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(int(20)))
        # fake_string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(int(varchar_length)))

    return fake_string_data


def gen_fake_numeric_data(row):

    fake_numeric_data = ''

    if row['data_type'].startswith('NUMBER'):

        split_str = row['data_type'].split('(')[1].split(',')
        precision = split_str[0]
        logger.debug(f'precision = {precision}')

        # if it's a 'quantity' field, limit to values 1-10
        if 'QUANTITY' in row['col_name'].upper():
            fake_numeric_data = random.randint(1, 10)
        # to facilitate table joins, limit IDs to a range of 10 values
        elif 'ID' in row['col_name'].upper():
            fake_numeric_data = random.randint(1, 10)
        # limit price to 100
        elif 'PRICE' in row['col_name'].upper():
            fake_numeric_data = str(f"'{random.randint(1, 100)}.00'")
        # limit year a value in the last 5 years
        elif 'YEAR' in row['col_name'].upper():
            fake_numeric_data = random.randint(date.today().year-5, date.today().year)
        else:
            # generating data to high precisions (e.g., 38) too big numbers. Limit to 50 and uncomment the line below if otherwise wanted.
            fake_numeric_data = random.randint(1, 50)

        # though if you do want to generate fake data to precision, use the below:
        # generate random number to (max) precision
        # fake_numeric_data = random.randint(1, 10**int(precision))

    return fake_numeric_data


def gen_fake_date_time_data(row):

    # TODO: multiple checks, e.g.: date vs datetime vs time?
    fake_date_time_data = ''

    fake_date_time_data = f"to_date('{fake_generator.date_between(current_dt_obj - timedelta(days=5), current_dt_obj)}')"

    return fake_date_time_data
