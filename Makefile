.PHONY: all build install upload

all: build install

edit:
	python install -e .

build:
	python -m build

install: 
	pip install .

upload: build
	twine upload dist/*

