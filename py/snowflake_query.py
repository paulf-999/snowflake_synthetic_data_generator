#!/usr/bin/env python
import inputs
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def create_snowflake_connection():
    # get inputs
    sf_username, sf_pass, sf_account, sf_wh, sf_role, sf_db, sf_db_schema = inputs.get_sf_conn_params()

    # uncomment this line if you're using a p8 key
    # sf_username, sf_p8_key_path, sf_account, sf_wh, sf_role, sf_db, sf_db_schema = inputs.get_sf_conn_params()

    # if a p8 key is used, render the key as required
    # if sf_p8_key_path:
    #     pkb = private_key_bytes(sf_p8_key_path)

    conn = snowflake.connector.connect(
        user=sf_username,
        password=sf_pass,
        # private_key=pkb,
        account=sf_account,
        warehouse=sf_wh,
        role='r_f_airflow_dev',
        database=sf_db,
        schema=sf_db_schema
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


# render private key for snowflake connection
def private_key_bytes(p8_key_path: str):
    with open(p8_key_path, 'rb') as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            None,
            backend=default_backend()
        )

    return p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


if __name__ == '__main__':
    """This is executed when run from the command line"""

    example_tbl = 'abc'

    get_table_schema(example_tbl)
