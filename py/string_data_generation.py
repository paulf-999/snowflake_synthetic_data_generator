import logging
import random
import string
from datetime import datetime

from faker import Faker
from faker.providers import address
from faker.providers import credit_card
from faker.providers import internet
from faker.providers import phone_number

# Set up a specific logger with our desired output level"""
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)

# create and initialize a faker generator. Ireland localisation arg provided
fake_data_generator = Faker('en_IE')  # TODO - parameterize this
fake_data_generator.add_provider(address)
fake_data_generator.add_provider(phone_number)
fake_data_generator.add_provider(credit_card)
fake_data_generator.add_provider(internet)


#####################################################################################################################
def gen_fake_string_person_data(row, fake_string_data=''):
    """generate fake string data, specifically person-type data"""

    if 'FIRST_NAME' in row['col_name'].upper():
        fake_string_data = fake_data_generator.first_name()
    # to facilitate table joins, limit IDs to a range of 10 values
    elif 'LAST_NAME' in row['col_name'].upper() or 'SURNAME' in row['col_name'].upper():
        fake_string_data = fake_data_generator.last_name()
    elif 'FULL_NAME' in row['col_name'].upper():
        fake_string_data = fake_data_generator.name()

    return fake_string_data


def gen_fake_string_location_data(row, fake_string_data=''):
    """generate fake string data, specifically location data"""

    if 'COUNTRY' in row['col_name'].upper():
        fake_string_data = fake_data_generator.current_country()
    elif 'STATE' in row['col_name'].upper():
        fake_string_data = fake_data_generator.state_abbr()
    elif 'CITY' in row['col_name'].upper():
        fake_string_data = fake_data_generator.city()
    elif 'TOWN' in row['col_name'].upper():
        fake_string_data = fake_data_generator.city_suffix()
    elif 'POSTCODE' in row['col_name'].upper() or 'POST_CODE' in row['col_name'].upper() or 'POSTALCODE' in row['col_name'].upper():
        fake_string_data = fake_data_generator.postcode()
    elif 'STREET' in row['col_name'].upper():
        fake_string_data = fake_data_generator.street_name()
    elif 'ADDRESS' in row['col_name'].upper():
        fake_string_data = fake_data_generator.street_address()

    return fake_string_data


def gen_fake_string_contact_details_data(row, fake_string_data=''):
    """generate fake string data, specifically contact detail data"""

    if 'PHONE' in row['col_name'].upper() or 'MOBILE' in row['col_name'].upper() or 'FAX' in row['col_name'].upper():
        fake_string_data = fake_data_generator.phone_number()
    elif 'EMAIL' in row['col_name'].upper():
        fake_string_data = fake_data_generator.ascii_free_email()

    return fake_string_data


def gen_fake_string_other_data(row, fake_string_data=''):
    """generate fake string data for other well-known use cases"""

    if 'EXPIRYDATE' in row['col_name'].upper() or 'EXPIRY_DATE' in row['col_name'].upper():
        fake_string_data = fake_data_generator.credit_card_expire()
    elif 'ID' in row['col_name'].upper():
        fake_string_data = str(random.randint(1, 10))
    # in case a date field is accidentally captured as a string, include data generation for it here
    elif 'DATE' in row['col_name'].upper():
        # TODO - try and randomise this value slightly
        fake_string_data = datetime.now()

    return fake_string_data


def gen_fake_default_string_data(row, fake_string_data=''):
    """generate fake string data for all other string data (i.e., for string data that doesn't match the above use cases)"""

    # generating a string to max length produces unreasonable/non-useful strings. Instead, try to limit to 10 where possible.
    varchar_length = row['data_type'].split('(')[1].split(')')[0]
    logging.info(f'varchar_length = {varchar_length}')

    # if a varchar length has been specified & is a reasonable length (i.e., < 200), generate a string to this length
    if int(varchar_length) < 200:
        fake_string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(int(varchar_length)))
    else:
        # else generate a string that is a reasonable length, e.g., 10 characters
        fake_string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(int(10)))

    return fake_string_data
