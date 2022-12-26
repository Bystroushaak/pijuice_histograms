#! /usr/bin/env bash

cp -r /code /tmp
cd /tmp/code
#dh $@ --python /usr/bin/python3
debuild -b -us -uc

mkdir -p /code/deb_build

find /tmp -name "*.deb" -exec cp {} /code/deb_build \;

chmod -R 777 /code/deb_build
