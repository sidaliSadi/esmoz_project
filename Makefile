.PHONY: requirements
requirements:
	pip install -r requirements.txt

unit-tests:
	PYTHONPATH=`pwd` pytest -s -vv tests/

run:
	PYTHONPATH=. python3 ./main.py