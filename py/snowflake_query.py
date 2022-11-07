#!/usr/bin/env python
import inputs
import snowflake.connector


def create_snowflake_connection():
    # get inputs
    snowflake_username, snowflake_pass, snowflake_account, snowflake_wh, snowflake_db, snowflake_db_schema = inputs.get_sf_conn_params()

    conn = snowflake.connector.connect(
        user=snowflake_username,
        password=snowflake_pass,
        account=snowflake_account,
        warehouse=snowflake_wh,
        database=snowflake_db,
        schema=snowflake_db_schema
    )

    return conn


def get_table_schema(input_tbl):
    """function to return the columns for a given input table, using a snowflake DESCRIBE query
    Output is written to: tmp/tables_schemas/{input_tbl}.csv
    """
    # establish a SF connection
    conn = create_snowflake_connection()
    cursor = conn.cursor()

    query = f'DESC table {input_tbl};'

    # write query output to the following file location
    with open(f'tmp/table_schemas/{input_tbl}.csv', 'w') as query_op:
        try:
            cursor.execute(query)
            query_result = cursor.fetchall()
            for tuple_result in query_result:

                for column in tuple_result:
                    query_op.write(f'{column};')

                query_op.write('\n')
        finally:
            cursor.close()
        conn.close()
