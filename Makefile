build: test flakes

setup:
	@pip install --requirement=requirements.txt

test:
	@env PYTHONHASHSEED=random PYTHONPATH=. nosetests --with-coverage --cover-min-percentage=100 --cover-package=sptrans --cover-erase --cover-html --with-yanc --with-xtraceback tests/

flakes:
	@flake8 . --ignore=E501