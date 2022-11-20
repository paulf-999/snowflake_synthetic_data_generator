# Snowflake Synthetic Data Generator

Python scripts to generate synthetic data in Snowflake, based upon a list of input tables provided. The scripts rely on reading the input table schemas to understand the name & data types of columns, to in turn use the Python library `Faker` to generate meaningful fake data.

## Summary

* For each input table listed in `ip/config.yaml`, these scripts generate X amount of fake data records.
  * Where X is based upon the value of `num_records_to_generate` in `ip/config.yaml`.
* The script reads the table schemas of each input table list provided to understand the name & data types of inputs columns, to in turn generate fake data.
* The script initially focusses on detecting the 5 groupings of Snowflake data types (see Summary of Data Types | docs.snowflake.com)[https://docs.snowflake.com/en/sql-reference/intro-summary-data-types.html] listed below:
  * String (i.e.: `VARCHAR`, `TEXT` and `STRING`)
  * Numeric (i.e.: `NUMBER`, `NUMERIC` and `DECIMAL`)
  * Date (i.e., `DATE`, `DATETIME`, `TIME`, `TIMESTAMP`, `TIMESTAMP_{LTZ}{_NTZ}{_TZ}`)
  * Boolean
  * Binary
* The script then inserts the generated fake data into each of the target tables.

---

### Technologies Used

* `Makefile`
* `Python`
* Python packages (see `requirements.txt`):
  * `snowflake-connector-python` - to query the Snowflake DB from the python script.
  * `Faker` - to generate fake data (see `py/dt_data_generation.py`).
  * `pandas` - to write Snowflake query output to Pandas data frames.
  * `pyyaml` & `yq` - to parse input from `config.yaml`
  * `cryptography` - to render an input private RSA key to query the Snowflake DB.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. Install the prerequisite python packages by running: `make deps`.
2. Provide values for each of the keys in ip/config.yaml. For a description breakdown of each of the input args, see `ip/README.md`.

## How-to Run

Run `make run` to:

* Write the table schemas for each input table listed underneath the `input_tbls` key in `ip/config.yaml`.
  * Note: the table schema output is written to `tmp/{input_tbl}.csv`. See the python function `get_table_schema()` in `snowflake_query.py` for more details.
* Generate X amount of fake data records (based upon the value of `num_records_to_generate` in `ip/config.yaml`) for each data type within each input table
  * Note: the generated fake data for each table is written to `op/{input_tbl}.csv`. See the function `generate_fake_data()` in `gen_fake_data.py` for more details.
* Insert the generated fake data into each of the target tables listed underneath the `input_tbls` key in `ip/config.yaml`.
  generate_fake_data
  * See the function `insert_fake_data()` in `gen_fake_data.py` for more details.

---

## Credits

This is an adapted version of the following [README](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc).
