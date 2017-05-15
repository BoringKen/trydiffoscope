FROM debian:sid

ENV DEBIAN_FRONTEND noninteractive

RUN echo CACHEBUST 1

RUN echo deb http://httpredir.debian.org/debian experimental main >> /etc/apt/sources.list
RUN apt-get update && apt-get dist-upgrade --yes
RUN apt-get install --yes --install-recommends --target-release=experimental diffoscope || apt-get install --yes --install-recommends diffoscope
