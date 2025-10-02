.PHONY: all build install upload

all: build install

build:
	python -m build

install: 
	pip install .

upload: build
	twine upload dist/*

