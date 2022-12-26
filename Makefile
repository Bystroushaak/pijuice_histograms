.PHONY: build
.PHONY: deploy

build:
	docker build -t python-deb-builder .
	docker run -v `pwd`:/code -it python-deb-builder /build_in_docker.sh

PKG_NAME := $(shell ls deb_build | sort | tail -n 1)
deploy: build
	scp deb_build/$(PKG_NAME) bystrousak@10.0.0.23:/home/bystrousak
	ssh bystrousak@10.0.0.23 "sudo dpkg -i $(PKG_NAME)"
