import os

import yaml


def read_ip():
    """Read input from config file"""
    working_dir = os.getcwd()

    with open(os.path.join(working_dir, 'ip', 'config.yaml')) as ip_yml:
        data = yaml.safe_load(ip_yml)

    return data


def get_general_params():
    """get 'general' params from input config"""
    data = read_ip()

    input_tbls = data['general_params']['input_tbls']
    num_records = data['general_params']['num_records_to_generate']

    return input_tbls, num_records


def get_sf_conn_params():
    """get snowflake db connections params from input config"""
    data = read_ip()

    sf_username = data['db_connection_params']['snowflake_username']
    sf_pass = data['db_connection_params']['snowflake_pass']
    # sf_p8_key_path = data['db_connection_params']['snowflake_p8_key']
    sf_account = data['db_connection_params']['snowflake_account']
    sf_wh = data['db_connection_params']['snowflake_wh']
    sf_role = data['db_connection_params']['snowflake_role']
    sf_db = data['db_connection_params']['snowflake_db']
    sf_db_schema = data['db_connection_params']['snowflake_db_schema']

    return sf_username, sf_pass, sf_account, sf_wh, sf_role, sf_db, sf_db_schema

    # return sf_username, sf_p8_key_path, sf_account, sf_wh, sf_role, sf_db, sf_db_schema = inputs.get_sf_conn_params()
