.PHONY: test bash build main


main: build
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis python src/main.py

build:
	docker build --tag titanic-data-analysis .

bash:
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis /bin/bash

test:
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis python test/main.py
