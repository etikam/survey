# Variables
PYTHON = python
MANAGE = $(PYTHON) manage.py

# Cibles
.PHONY: migrate makemigrations run

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

runs:
	$(MANAGE) runserver
