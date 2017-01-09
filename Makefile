init:
	pip3 install -r requirements.txt

test:
	nosetests --with-coverage --cover-html --cover-package yaz

.PHONY: init test
