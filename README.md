# Snowflake Synthetic Data Generator

Python scripts to create synthetic data in Snowflake, based upon a list of input table schemas provided.

## Summary

* For each input table listed in `ip/config.yaml`, these scripts generate X amount of fake data records.
  * Where X is based upon the value of `num_records_to_generate` in `ip/config.yaml`.
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
  * Note: the table schema output is written to `tmp/{input_tbl}.csv`.
  * See the python function `get_table_schema()` in `snowflake_query.py`.
* Generate X amount of fake data records (based upon the value of `num_records_to_generate` in `ip/config.yaml`) for each data type within each input table
  * Note: the generated fake data for each table is written to `op/{input_tbl}.csv`.
  * See the function `generate_fake_data()` in `gen_fake_data.py`.
* Insert the generated fake data into each of the target tables listed underneath the `input_tbls` key in `ip/config.yaml`.
  generate_fake_data
  * See the function `insert_fake_data()` in `gen_fake_data.py`.

---

## Credits

This is an adapted version of the following [README](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc).
