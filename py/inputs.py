import os

import yaml


def read_ip():
    """Read input from config file"""
    working_dir = os.getcwd()

    with open(os.path.join(working_dir, 'ip', 'config_mine.yaml')) as ip_yml:
        # with open(os.path.join(working_dir, 'ip', 'config_mine.yaml')) as ip_yml:
        data = yaml.safe_load(ip_yml)

    return data


def get_general_params():
    """get 'general' params from input config"""
    data = read_ip()

    data_src = data['general_params']['data_src']
    num_records = data['general_params']['num_records_to_generate']

    # data_src table specific key/values
    data_src_ip_tbls = {}
    data_src_ip_tbls['data_src_a'] = data['data_src_tables']['data_src_a_tables']

    return data_src, data_src_ip_tbls, num_records


def get_sf_conn_params(data_src):
    """get snowflake db connections params from input config"""
    data = read_ip()

    # store the credentials in a py dictionary
    sf_conn_details = {}

    sf_conn_details['sf_username'] = data['db_connection_params']['snowflake_username']
    sf_conn_details['sf_pass'] = data['db_connection_params']['snowflake_pass']
    # sf_conn_details["sf_p8_key_path"] = data['db_connection_params']['snowflake_p8_key']
    # sf_conn_details["sf_p8_key_passphrase"] = data['db_connection_params']['snowflake_p8_key_passphrase']
    sf_conn_details['sf_account'] = data['db_connection_params']['snowflake_account']
    sf_conn_details['sf_wh'] = data['db_connection_params']['snowflake_wh']
    sf_conn_details['sf_role'] = data['db_connection_params']['snowflake_role']
    sf_conn_details['sf_db'] = data['db_connection_params']['snowflake_db']
    sf_conn_details['sf_db_schema'] = data['db_connection_params']['snowflake_db_schema']

    return sf_conn_details
