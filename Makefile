SHELL = /bin/sh

# Usage:
# make installations	# install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup

# all: deps install [X, Y, Z...] clean

.EXPORT_ALL_VARIABLES:
.PHONY = installations deps install clean get_ips validate_user_ip

CONFIG_FILE := ip/config.yaml
# the 2 vars below are just for formatting CLI message output
COLOUR_TXT_FMT_OPENING := \033[0;33m
COLOUR_TXT_FMT_CLOSING := \033[0m

installations: deps clean run

deps: get_ips
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@echo "${COLOUR_TXT_FMT_OPENING}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_TXT_FMT_CLOSING}"
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@pip3 install -r requirements.txt -q
	@pip3 install yq -q

run: clean get_ips
	@echo "------------------------------------------------------------------"
	@echo "${COLOUR_TXT_FMT_OPENING}Target: 'run'. Run the execution script.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@python3 py/gen_fake_data.py

clean:
	@echo "------------------------------------------------------------------"
	@echo "${COLOUR_TXT_FMT_OPENING}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@rm -rf tmp/*.csv
	@rm -rf op/*.csv

#############################################################################################
# Setup/validation targets: 'get_ips' & 'validate_user_ip'
#############################################################################################
get_ips:
	@echo "------------------------------------------------------------------"
	@echo "${COLOUR_TXT_FMT_OPENING}Target: 'get_ips'. Get input args from config.yaml.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	$(eval CURRENT_DIR=$(shell pwd))
	$(eval ENV=$(shell yq -r '.general_params.env | select( . != null )' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo "------------------------------------------------------------------"
	@echo "${COLOUR_TXT_FMT_OPENING}Target: 'validate_user_ip'. Validate the user inputs.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	# INFO: Verify the user has provided a value for the key 'env' in ip/config.yaml
	@[ "${ENV}" ] || ( echo "\nError: 'ENV' key is empty in ip/config.yaml\n"; exit 1 )

# WIP
run_pytests:
	pytest -rA tests/ --no-header --disable-pytest-warnings --color=yes
