#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : gen_fake_data.py
* Description   : Script to create synthetic data in Snowflake, based upon the list of input table schemas
* Created       : 07-11-2022
* Usage         : python3 gen_fake_data.py
"""

__author__ = 'Paul Fry'
__version__ = '1.0'

import logging
import os

# custom modules
import snowflake_client

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)


def validate_db_connectivity(data_src):
    """validate connectivity to SF db"""

    sf_query_op = snowflake_client.snowflake_query(query='SELECT current_version();', data_src=data_src)
    logger.debug(f'sf_query_op = {sf_query_op}')
    logger.info('\nINFO: Connectivity to SF db confirmed.\n')

    return


def write_ip_table_schema_to_tmp(data_src, input_tbl):
    """get the input table's schema definition & write it to a file in the tmp folder"""

    # verify the target dir exists
    target_dir = f'tmp/{data_src}/'
    verify_dir_exists(target_dir)

    with open(f'{target_dir}/{input_tbl}.csv', 'w') as tmp_sf_tbl_schema:
        # fetch the schema of the given input table
        sf_query_op = snowflake_client.snowflake_query(query=f'DESC table {input_tbl};', data_src=data_src)

        tmp_sf_tbl_schema.write(sf_query_op)

    return


def generate_truncate_tbl_statements(data_src, input_tbl, trunc_tbl_sql, len_ip_tbls, write_mode=''):
    """for each input table, generate a 'TRUNCATE TABLE statement to aid later troubleshooting"""

    trunc_tbl_sql = f'TRUNCATE TABLE {input_tbl};\n'
    logger.debug(trunc_tbl_sql)

    target_file_path = f'op/truncate_tbl_statements/truncate_{data_src}_tbls.sql'

    if (os.path.exists(target_file_path)):
        num_lines = sum(1 for line in open(target_file_path))
        logger.debug(f'len_ip_tbls = {len_ip_tbls}. num_lines = {num_lines}')

        # the file already existed with values = overwrite it. Also append.
        if num_lines == len_ip_tbls:
            write_mode = 'w'
        else:
            write_mode = 'a'

    # the file didn't previously exist, create it
    else:
        write_mode = 'w'

    with open(target_file_path, write_mode) as op_sql:
        op_sql.write(trunc_tbl_sql)

    return trunc_tbl_sql


def execute_generated_sql(data_src, ip_tbls, generated_sf_query=''):
    """iterate through each of the input tables to now execute the 'INSERT INTO' statements"""

    logger.info('\n#########################################################')
    logger.info('# Start sequence for inserting the generated data.')
    logger.info('#########################################################\n')

    for input_tbl in ip_tbls:

        logger.info(f"Insert fake data for: '{input_tbl}'.")

        with open(f'op/{data_src}/insert_statements/{input_tbl}.sql') as ip_sql:
            generated_sf_query = ip_sql.read()

        # execute the sf query
        snowflake_client.snowflake_query(query=generated_sf_query, data_src=data_src)

    return


def verify_dir_exists(target_dir):
    """create the target dir if it doesn't exist"""
    if not os.path.exists(target_dir):
        logger.info(f"Target directory '{target_dir}' doesn't exist - will create it.")
        os.makedirs(target_dir)

    return
