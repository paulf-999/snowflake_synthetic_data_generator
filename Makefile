SHELL = /bin/sh

# Usage:
# make installations	# install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup

.EXPORT_ALL_VARIABLES:
.PHONY = installations deps install clean get_ips validate_user_ip

CONFIG_FILE := ip/config.yaml
# the 2 vars below are just for formatting CLI message output
COLOUR_TXT_FMT_OPENING := \033[0;33m
COLOUR_TXT_FMT_CLOSING := \033[0m

installations: deps clean run

deps: get_ips
	@echo -e "----------------------------------------------------------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_TXT_FMT_CLOSING}"
	@echo -e "----------------------------------------------------------------------------------------------------------------------"
	@virtualenv -p python3 venv; \
	source venv/bin/activate; \
	pip3 install -r requirements.txt; \

run: clean get_ips
	@echo -e "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'run'. Run the execution script.${COLOUR_TXT_FMT_CLOSING}"
	@echo -e "------------------------------------------------------------------"
	@python3 py/gen_fake_data.py

clean: get_ips
	@echo -e "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_TXT_FMT_CLOSING}"
	@echo -e "------------------------------------------------------------------"
	@rm -rf tmp/${DATA_SRC}/ && rm -rf op/${DATA_SRC}/insert_statements/

#############################################################################################
# Setup/validation targets: 'get_ips' & 'validate_user_ip'
#############################################################################################
get_ips:
	@echo -e "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'get_ips'. Get input args from config.yaml.${COLOUR_TXT_FMT_CLOSING}"
	@echo -e "------------------------------------------------------------------"
	$(eval CURRENT_DIR=$(shell pwd))
	$(eval ENV=$(shell yq -r '.general_params.env | select( . != null )' ${CONFIG_FILE}))
	$(eval DATA_SRC=$(shell yq -r '.general_params.data_src | select( . != null )' ${CONFIG_FILE}))
	$(eval FAKER_COUNTRY=$(shell yq -r '.general_params.data_src | select( . != null )' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo -e "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'validate_user_ip'. Validate the user inputs.${COLOUR_TXT_FMT_CLOSING}"
	@echo -e "------------------------------------------------------------------"
	# INFO: Verify the user has provided a value for the key 'env' in ip/config.yaml
	@[ "${ENV}" ] || ( echo "\nError: 'ENV' key is empty in ip/config.yaml\n"; exit 1 )
	# INFO: Verify the user has provided a value for the key 'data_src' in ip/config.yaml
	@[ "${DATA_SRC}" ] || ( echo "\nError: 'ENV' key is empty in ip/config.yaml\n"; exit 1 )

# WIP
run_pytests:
	pytest -rA tests/ --no-header --disable-pytest-warnings --color=yes
