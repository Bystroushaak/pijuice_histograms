.PHONY: build

build:
	docker build -t python-deb-builder .
	docker run -v `pwd`:/code -it python-deb-builder /build_in_docker.sh
