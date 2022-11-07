# Prerequisites

Described below are the input config parameters read in from `ip/config.yaml` by the synthetic data generation scripts.

## General Parameters

| Parameter | Description | Example                  |
| --------- | ---------------------------- | ------- |
| env | Name of the environment | `dev` |
| input_tbls | List of the (data source) input tables (used by the .py generation scripts) | `input_tbls:`<br/>`- table_a`<br/>`- table_b` |

## DB Connection Parameters

| Parameter | Description                  | Example |
| --------- | ---------------------------- | ------- |
| snowflake_account | The Snowflake account name. | `<company_abc>.ap-southeast-2` |
| snowflake_username | Snowflake username.<br/>Update this to reflect your own Snowflake username. | `jbloggs@email.com` |
| snowflake_pass | Snowflake password.<br/>Update this to reflect your own Snowflake password. | `<your_password>` |
| snowflake_p8_key | Your generated RSA key.<br/>Update this to reflect the name of your RSA key. | `example_rsa_key.p8` |
| snowflake_wh | Snowflake warehouse to use. | `wh_sf_role_wh_xs_${ENV}` |
| snowflake_role | Snowflake role to use. | `svc_sf_role_${ENV}` |
| snowflake_src_db | Snowflake DB for the data_src. | `${DATA_SRC}_${ENV}` |
| snowflake_src_db_schema | Snowflake DB schema for the data_src | `landed` |
