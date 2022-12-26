FROM ubuntu:focal

RUN apt-get update \
 && apt-get install -y software-properties-common gpg \
 && add-apt-repository ppa:jyrki-pulliainen/dh-virtualenv \
 && apt-get update

RUN apt-get install -y dh-virtualenv devscripts debhelper dh-python python3-virtualenv devscripts python3-setuptools \
 && apt-get clean

COPY build_in_docker.sh /
