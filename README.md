# Snowflake Synthetic Data Generator

Python scripts to create synthetic data in Snowflake, based upon the list of input table schemas.

---

## Technologies Used

* Makefile
* Python
* The Python packages (see `requirements.txt`):
  * `snowflake-connector-python` - to query the Snowflake DB from the python script.
  * `pandas` - to write Snowflake query output to Pandas data frames.
  * `pyyaml` & `yq` - to parse input from `config.yaml`
  * `cryptography` - to render an input private RSA key to query the Snowflake DB.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. Install the prerequisite python packages by running: `make deps`.
2. Provide values for each of the keys in ip/config.yaml. For a description breakdown of each of the input args, see `ip/README.md`.

## How-to Run

Run `make install` to:

* Write the table schemas for each input table listed underneath the `input_tbls` key in `ip/config.yaml`.
* Generate X amount of fake data records (based upon the value of `num_records_to_generate` in `ip/config.yaml`) for each data type within each input table
* Insert the generated fake data into each of the target tables listed underneath the `input_tbls` key in `ip/config.yaml`.

---

## Credits

This is an adapted version of the following [README](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc).
