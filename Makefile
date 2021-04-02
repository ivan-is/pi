PYTHON=python3.7
VERSION=`python setup.py --version`

.PHONY: up
up:
	@cd ansible && ansible-playbook -v playbooks/up.yaml

.PHONY: down
down:
	@cd ansible && ansible-playbook -v playbooks/down.yaml

.PHONY: reboot
reboot:
	@cd ansible && ansible-playbook playbooks/reboot.yaml

.PHONY: pre_install
pre_install:
	@cd ansible && ansible-playbook playbooks/raspi_config.yaml
	@cd ansible && ansible-playbook playbooks/update.yaml

.PHONY: install
install: pre_install reboot
	@cd ansible && ansible-playbook playbooks/install.yaml

.PHONY: dev
dev:
	@pip3 -r requirements.txt
	# install an Ansible role which automates setting up Docker
	@ansible-galaxy install geerlingguy.docker_arm
