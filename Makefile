.PHONY: test bash build train_model test_model

LOGLEVEL ?= INFO
LOGGING_CMD = --log=${LOGLEVEL}

test_model: build
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis python src/main.py --train-dataset=train.csv --test-dataset=test.csv ${LOGGING_CMD}

train_model: build
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis python src/main.py --dataset=train.csv --log=DEBUG

build: Dockerfile
	docker build --tag titanic-data-analysis .

Dockerfile: utils/base.Dockerfile utils/createDockerImage.py
	@read -p "Would you like to enable X11 forwarding? (y, N): " usr_input; \
	if [ "$$usr_input" == "y" ]; then cmdargs="--xServer"; fi; \
	cd utils && python createDockerImage.py $$cmdargs --procs=$$(nproc)

bash:
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis /bin/bash

test:
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis python test/main.py

clean:
	-rm -rf data/out/*.csv
	-rm -rf data/out/graphs/*.png
