#!/usr/bin/env python
import logging

import inputs
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from snowflake.connector.errors import DatabaseError
from snowflake.connector.errors import ProgrammingError

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)


def create_snowflake_connection(conn=''):
    """create a sf connection instance"""
    # get inputs
    sf_conn_details = inputs.get_sf_conn_params()

    # if a p8 key is used, render the key as required
    # pkb = private_key_bytes(sf_conn_details["sf_p8_key_path"], sf_conn_details["sf_p8_key_passphrase"])

    try:
        conn = snowflake.connector.connect(
            user=sf_conn_details['sf_username'],
            password=sf_conn_details['sf_pass'],
            # private_key=sf_conn_details["sf_p8_key_path"],
            account=sf_conn_details['sf_account'],
            warehouse=sf_conn_details['sf_wh'],
            role=sf_conn_details['sf_role'],
            database=sf_conn_details['sf_db'],
            schema=sf_conn_details['sf_db_schema'],
        )

    except ProgrammingError as e:
        if e.errno == 251005:
            print(f"\nERROR: Invalid username/password.\n\nMessage: '{e.msg}'.")
            raise (SystemExit)
        else:
            print(f'Error {e.errno} ({e.sqlstate}): ({e.sfqid})')
            raise (SystemExit)

    except DatabaseError as db_e:
        if db_e.errno == 250001:
            print(f"\nERROR: Invaid Snowflake account name provided.\n\nMessage: '{db_e.msg}'.")
            raise (SystemExit)
        else:
            print(f'Error {db_e.errno} ({db_e.sqlstate}): ({db_e.sfqid})')
            raise (SystemExit)

    return conn


def snowflake_query(query, sf_query_op=''):
    """Connect to SF DB & run query"""

    # establish a SF connection
    conn = create_snowflake_connection()

    cursor = conn.cursor()

    try:
        cursor.execute(query)
        query_result = cursor.fetchall()
        logger.debug(f'query_result = {query_result}')
        for tuple_result in query_result:

            for column in tuple_result:
                sf_query_op += f'{column};'
            sf_query_op += '\n'
    finally:
        cursor.close()
    conn.close()

    return sf_query_op


def private_key_bytes(p8_key_path, p8_passphrase):
    """render private key for snowflake connection"""
    with open(p8_key_path, 'rb') as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            p8_passphrase,
            backend=default_backend()
        )

    return p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


if __name__ == '__main__':
    """This is executed when run from the command line"""

    snowflake_query(query='SELECT current_version();')
