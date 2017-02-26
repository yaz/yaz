init:
	pip install -r requirements.txt

test:
	nosetests --with-coverage --cover-html --cover-package yaz

upload: test
	python setup.py sdist upload -r pypi

.PHONY: init test upload
