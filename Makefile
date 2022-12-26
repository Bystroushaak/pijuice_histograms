.PHONY: build
.PHONY: deploy
.PHONY: changelog

build:
	docker build -t python-deb-builder .
	docker run -v `pwd`:/code -it python-deb-builder /build_in_docker.sh

deploy: build
	PKG_NAME=`ls deb_build | sort | tail -n 1`; \
	scp deb_build/$${PKG_NAME} bystrousak@10.0.0.23:/home/bystrousak && \
	ssh bystrousak@10.0.0.23 "sudo dpkg -i $${PKG_NAME}"

changelog:
	dch -m -U
