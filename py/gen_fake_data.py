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
import sql_functions

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('application_logger')
logger.setLevel(logging.INFO)


def process_generated_sql(generated_sql, row, column_count, df, fake_data):
    """repeated orchestration logic used for every data type's fake data generation"""

    # append the generated output to the SQL 'insert into' statement
    logger.debug(f'column_count= {column_count}')

    # put quotes around the var `fake_data` if it's a string
    if row['data_type'].startswith('VARCHAR'):
        fake_data = f"'{fake_data}'"

    # determine whether fake data has been generated for all cols in the df
    if column_count != len(df):
        logger.debug(f"column_count doesn't match, len(df) = {len(df)}")
        generated_sql += f'{fake_data}, '
        column_count += 1
    elif column_count == len(df):
        logger.debug(f'column_count MATCHES, len(df) = {len(df)}')
        generated_sql += f'{fake_data}'

    return generated_sql, column_count


def orchestrate_fake_data_generation(input_tbl, df, num_records):
    """For a given input table, generate X (num_records) fake records"""

    logger.debug(f'len(df) = {len(df)}')

    # verify the target dir exists
    target_dir = f'op/{data_src}/insert_statements/'
    sql_functions.verify_dir_exists(target_dir)

    # generated_sql will be continually be appended to in orchestrate_fake_data_generation()
    generated_sql = f'INSERT INTO {input_tbl.upper()} VALUES \n'

    # generate the fake data for the amount of rows specified by `num_records`
    for row_to_generate in range(0, int(num_records)):

        # reset the column count for each record being generated
        column_count = 1
        generated_sql += '('

        # Determine the data types of the table schema
        for index, row in df.iterrows():

            logger.debug(f"col_name: {row['col_name']}\tdata_type: {row['data_type']}")

            # these 3 vars are lists used to store generated fake data
            fake_numeric_data = fake_string_data = fake_time_data = []

            if row['data_type'].startswith('VARCHAR') or row['data_type'].startswith('TEXT') or row['data_type'].startswith('STRING'):
                logger.debug('Data type = string')
                fake_string_data = dt_generator.orchestrate_gen_fake_string_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_string_data)

            elif row['data_type'].startswith('NUMBER') or row['data_type'].startswith('NUMERIC'):
                logger.debug('Data type = number')
                fake_numeric_data = dt_generator.gen_fake_numeric_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_numeric_data)

            elif row['data_type'].startswith('DATE') or row['data_type'].startswith('TIME'):
                logger.debug('Data type = timestamp')
                fake_time_data = dt_generator.gen_fake_date_time_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_time_data)

            elif row['data_type'].startswith('BOOLEAN'):
                logger.debug('Data type = boolean')
                fake_boolean_data = dt_generator.gen_fake_boolean_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_boolean_data)

            elif row['data_type'].startswith('BINARY'):
                logger.info('Data type = binary')
                logger.info('################################################################')
                logger.info('INFO: This query requires manual intervention, due to different syntax used')
                logger.info('See: https://docs.snowflake.com/en/sql-reference/sql/insert.html#usage-notes')
                logger.info('################################################################')
                fake_binary_data = dt_generator.gen_fake_binary_data(row)

                # append the generated output to the SQL 'insert into' statement
                generated_sql, column_count = process_generated_sql(generated_sql, row, column_count, df, fake_binary_data)

        logger.debug(f'int(num_records) = {int(num_records)}')
        logger.debug(f'row_to_generate = {int(row_to_generate)+1}')

        if int(row_to_generate)+1 != int(num_records):
            generated_sql += '),\n'
        else:
            generated_sql += ');'

    with open(f'{target_dir}/{input_tbl}.sql', 'w') as op_sql:
        logger.debug(generated_sql)
        op_sql.write(generated_sql)


def read_sf_table_schema_to_df(data_src, input_tbl):
    """read the input table schema into a pandas data frame (df)"""

    # sf table schema for 'describe() function output
    col_names = ['col_name', 'data_type', 'kind', 'null', 'default', 'primary_key', 'unique_key', 'check', 'expression', 'comment', 'policy_name', '-']  # noqa

    df = pd.read_csv(f'tmp/{data_src}/{input_tbl}.csv', sep=';', names=col_names).reset_index()
    logger.debug(df)

    return df


def main(data_src, ip_tbls, trunc_tbl_sql=''):
    """ Main program orchestration logic used to generate the fake data.
    # Iterate through each of the input tables to:
    # * fetch the input table schema
    # * generate fake data for each column data type
    # * generate the SQL 'insert into' statement
    # * generate SQL 'truncate table' statements to aid troubleshooting
    """
    for input_tbl in ip_tbls:

        # write logging message to console
        logger.debug(f"\nGenerating fake data for: {data_src} - '{input_tbl}'.\n")

        # write input table schema to the tmp folder
        sql_functions.write_ip_table_schema_to_tmp(data_src, input_tbl)

        # read the input table schema into a pandas data frame (df).
        df = read_sf_table_schema_to_df(data_src, input_tbl)

        # orchestrate the fake data generation logic, per column data type
        orchestrate_fake_data_generation(input_tbl, df, num_records)

        # to aid troubleshooting, also generate a master SQL truncate table statement
        trunc_tbl_sql += sql_functions.generate_truncate_tbl_statements(data_src, input_tbl, trunc_tbl_sql, len(ip_tbls))

    return


if __name__ == '__main__':
    """This is executed when run from the command line"""

    # get 'general' params from input config
    data_src, data_src_ip_tbls, num_records = inputs.get_general_params()

    # initialise var
    ip_tbls = ''

    # fetch only the input tables for the data source we're interested in
    for dict_data_src, src_tables in data_src_ip_tbls.items():
        if data_src == dict_data_src:
            ip_tbls = src_tables
    logger.info(f'INFO:\ndata_src = {data_src}. ip_tbls = {ip_tbls}')

    # validate connectivity to SF db
    sql_functions.validate_db_connectivity(data_src)

    # invoke main() to orchestrate the processing logic to generate fake data
    main(data_src, ip_tbls)

    # Start sequence for inserting the generated data.
    sql_functions.execute_generated_sql(data_src, ip_tbls)

    logger.info('\n#########################################################')
    logger.info('Finished! Check target tables.')
    logger.info('#########################################################\n')
