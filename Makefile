.PHONY: install, db-setup, help, format, lint


isort = isort app.py peskos tests
black = black app.py peskos tests
flake8 = flake8 app.py peskos tests
mypy = mypy app.py peskos tests


install:
	pip install -r requirements.txt

run:
	python app.py

db-setup:
	flask db stamp head
	flask db upgrade

format:
	$(isort)
	$(black)

lint:
	$(flake8)
	$(isort) --check-only
	$(black) --check
	$(mypy)
