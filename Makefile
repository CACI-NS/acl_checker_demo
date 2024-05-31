.DEFAULT_GOAL := help

export ANSIBLE_HOST_KEY_CHECKING=False
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PATH=$$PATH:./venv/bin:/usr/local/bin:/usr/bin:/bin

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'
	
.PHONY: install-deps
install-deps: ## Install pip
	apt-get update -y
	apt-get install python3-pip -y
	apt install python3.8-venv -y
	
.PHONY: add-venv
add-venv: ## Install virtualenv, create virtualenv, install requirements
	python3 -m venv venv
	. ./venv/bin/activate
	@echo installing requirements.txt ...
	@venv/bin/pip install -r ./requirements.txt

.PHONY: batfish-test
batfish-test: ## Execute batfish testing
	. ./venv/bin/activate
	python validate_acls.py

.PHONY: remove-venv
remove-venv: ## Remove virtualenv
	. ./venv/bin/activate
	rm -rf ./venv
