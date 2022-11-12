import logging
import random
from datetime import date
from datetime import datetime
from datetime import timedelta

import string_data_generation
from faker import Faker

# Set up a specific logger with our desired output level"""
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)

# create and initialize a faker generator. Ireland localisation arg provided
fake_data_generator = Faker('en_IE')  # TODO - parameterize this

# the current data/time is used in several places in this script
current_dt_obj = datetime.now()


def orchestrate_gen_fake_string_data(row, fake_string_data=''):
    """generate fake string data for a given string field"""

    ##########################################################
    # Person-specific fake data (using Faker)
    ##########################################################
    for substring in ['FIRST_NAME', 'LAST_NAME', 'SURNAME', 'FULL_NAME']:
        if row['col_name'].upper() in substring:
            logger.debug('Called gen_fake_string_person_data()')
            fake_string_data = string_data_generation.gen_fake_string_person_data(row)

    ##########################################################
    # Location-specific fake data (using Faker)
    ##########################################################
    for substring in ['COUNTRY', 'STATE', 'CITY', 'TOWN', 'POSTCODE', 'POST_CODE', 'POSTALCODE', 'STREET', 'ADDRESS']:
        if row['col_name'].upper() in substring:
            logger.debug('Called gen_fake_string_location_data()')
            fake_string_data = string_data_generation.gen_fake_string_location_data(row)

    ##########################################################
    # Contact details-specific fake data (using Faker)
    ##########################################################
    for substring in ['PHONE', 'MOBILE', 'FAX', 'EMAIL']:
        if row['col_name'].upper() in substring:
            logger.debug('Called gen_fake_string_contact_details_data()')
            fake_string_data = string_data_generation.gen_fake_string_contact_details_data(row)

    ##########################################################
    # Other fake data (using Faker)
    ##########################################################
    for substring in ['EXPIRYDATE', 'EXPIRY_DATE', 'ID', 'DATE']:
        if row['col_name'].upper() in substring:
            logger.debug('Called gen_fake_string_other_data()')
            fake_string_data = string_data_generation.gen_fake_string_other_data(row)

    logger.info(f'fake_string_data = {fake_string_data}')

    # If `fake_string_data` hasn't yet been populated, it means there hasn't been a match to any of the above scenarios.
    # As such, we should generate a random string for all other string data
    if len(fake_string_data) == 0:
        logger.debug('Called gen_fake_default_string_data()')
        fake_string_data = string_data_generation.gen_fake_default_string_data(row)

    return fake_string_data


def gen_fake_numeric_data(row, fake_numeric_data=''):
    """generate fake numeric data for a given numeric field"""

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
    # generate fake numeric data for everything else
    else:
        # Limit to generated number range to 50. I found generating numbers to the precision values generated (not useful) huge values.
        fake_numeric_data = random.randint(1, 50)

        # though if you do want to generate fake data to precision, use the below:
        """
        split_str = row['data_type'].split('(')[1].split(',')
        precision = split_str[0]
        logger.debug(f'precision = {precision}')

        # generate random number to (max) precision
        # fake_numeric_data = random.randint(1, 10**int(precision))
        """

    return fake_numeric_data


def gen_fake_date_time_data(row, fake_time_data=''):
    """generate fake data/time data for a given date/time field"""

    fake_time_data = f"to_date('{fake_data_generator.date_between(current_dt_obj - timedelta(days=5), current_dt_obj)}')"

    # TODO: add further checks/types of date/time data to generate, e.g., values for date vs time vs datetime?

    return fake_time_data


def gen_fake_boolean_data(row):
    """generate fake boolean data for a given boolean field"""

    valid_values = [1, 0]

    fake_boolean_data = random.choice(valid_values)

    return fake_boolean_data


def gen_fake_binary_data(row):
    """generate fake binary data for a given boolean field"""

    # for reference, see: https://docs.snowflake.com/en/sql-reference/functions/hex_decode_string.html

    fake_binary_data = "HEX_ENCODE('abc')"

    return fake_binary_data
