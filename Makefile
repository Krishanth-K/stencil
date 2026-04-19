.PHONY: all build install upload

all: build install

edit:
	pip install -e .

build:
	python -m build

install: 
	pip install .

upload: build
	twine upload dist/*

