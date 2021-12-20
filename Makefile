SHELL := /bin/bash
.SHELLFLAGS = -ec
.SILENT:
MAKEFLAGS += --silent
.ONESHELL:
.DEFAULT_GOAL: help

help:
	echo -e "Please use \`make \033[36m<target>\033[0m\`"
	echo -e "👉\t where \033[36m<target>\033[0m is one of"
	grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = "(: |##)"}; {printf "• \033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: init-day ## Create files for given DAY (use DAY=XX make init-day)
init-day:
	mkdir "d${DAY}"
	touch "d${DAY}/main.py"
	touch "d${DAY}/input"
	touch "d${DAY}/test_input"