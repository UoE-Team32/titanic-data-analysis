.PHONY: test bash build main


main: build
	docker run --rm -it --volume "$$(pwd)":/app titanic-data-analysis python src/main.py

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
	-rm -rf data/out/*
