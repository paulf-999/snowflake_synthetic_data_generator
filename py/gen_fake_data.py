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
import pandas as pd

# custom modules
import inputs
import dt_data_generation as dt_generator
import snowflake_client

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)


def insert_fake_data():
    """Insert generated fake data into target table"""

    logger.debug('Hello, world!')

    return


def process_generated_sql(generated_sql, row, column_count, df, fake_data):
    """repeated orchestration logic used for every (data type) fake data generation"""

    # append the generated output to the SQL 'insert into' statement
    logger.debug(f'column_count= {column_count}')

    # put quotes around the var `fake_data` if it's a string
    if row['data_type'].startswith('VARCHAR'):
        fake_data = f"'{fake_data}'"

    # determine whether fake data has been generated for all cols in the df
    if column_count != len(df):
        generated_sql += f'{fake_data}, '
        column_count += 1
    else:
        generated_sql += f'{fake_data}'

    return generated_sql, column_count


def generate_fake_data(input_tbl, df, num_records):
    """For a given input table, generate X (num_records) fake records"""

    logger.debug(f'len(df) = {len(df)}')

    # generated_sql will be continually be appended to in orchestrate_fake_data_generation()
    generated_sql = f'INSERT INTO {input_tbl.upper()} VALUES \n'

    # generate the fake data for the amount of rows specified by `num_records`
    for row_to_generate in range(0, int(num_records)):

        # reset the column count for each record being generated
        column_count = 1
        generated_sql += '('

        # Determine the data types of the table schema
        for index, row in df.iterrows():

            # generated_sql += orchestrate_fake_data_generation(row, generated_sql, df, column_count=1)

            logger.info(f"col_name: {row['col_name']}\tdata_type: {row['data_type']}")

            # these 3 vars are lists used to store generated fake data
            fake_numeric_data = fake_string_data = fake_date_time_data = []

            if row['data_type'].startswith('VARCHAR'):
                logger.debug(r'\Data type = string')
                fake_string_data = dt_generator.gen_fake_string_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_string_data)

            if row['data_type'].startswith('NUMBER'):
                logger.debug(r'\Data type = number')
                fake_numeric_data = dt_generator.gen_fake_numeric_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_numeric_data)

            if row['data_type'].startswith('TIMESTAMP'):
                logger.debug(r'\Data type = timestamp')
                fake_date_time_data = dt_generator.gen_fake_date_time_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_date_time_data)

        generated_sql += ')\n'
    generated_sql += ';'

    with open(f'op/{input_tbl}.sql', 'w') as op_sql:
        logger.debug(generated_sql)
        op_sql.write(generated_sql)


def read_table_schema(input_tbl):
    """read the table schema into a df"""

    # sf table schema for 'describe() function output
    col_names = [
        'col_name', 'data_type', 'kind', 'null', 'default', 'primary_key', 'unique_key', 'check', 'expression', 'comment', 'policy_name', '-'
    ]

    df = pd.read_csv(f'tmp/{input_tbl}.csv', sep=';', names=col_names).reset_index()
    logger.debug(df)

    return df


if __name__ == '__main__':
    """This is executed when run from the command line"""

    # get 'general' params from input config
    input_tbls, num_records = inputs.get_general_params()

    # validate connectivity to SF db
    sf_query_op = snowflake_client.snowflake_query(query='SELECT current_version();')
    logger.debug(f'sf_query_op = {sf_query_op}')
    logger.info('\nINFO: Connectivity to SF db confirmed.')

    for input_tbl in input_tbls:

        # write logging message to console
        logger.info(f"\nGenerating fake data for: '{input_tbl}'.\n")

        # write the query output to the tmp folder
        with open(f'tmp/{input_tbl}.csv', 'w') as tmp_sf_tbl_schema:
            # fetch the schema of the given input table
            sf_query_op = snowflake_client.snowflake_query(query=f'DESC table {input_tbl};')
            tmp_sf_tbl_schema.write(sf_query_op)

        # read the table schema into a df
        df = read_table_schema(input_tbl)

        # invoke the main orchestration logic per-input table
        generate_fake_data(input_tbl, df, num_records)

        # TODO: insert the fake data
        insert_fake_data()
