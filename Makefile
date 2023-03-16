.PHONY: install, db-setup, help

install:
	pip install -r requirements.txt

run:
	python app.py

db-setup:
	flask db stamp head
	flask db upgrade
