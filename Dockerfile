FROM ubuntu:18.04
MAINTAINER Alexandre Savio <alexsavio@gmail.com>

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64 /usr/bin/dumb-init
RUN chmod +x /usr/bin/dumb-init

## Configure default locale
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install -qq -y build-essential libssl-dev libxrender-dev libffi-dev \
                              libxml2-dev libxslt-dev \
                              wget git \
                              python3 python3-pip inkscape && \
    pip3 install -U pip setuptools pipenv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY eptools/badges/data/ep2018/fonts/*.ttf /usr/local/share/fonts/truetype/

RUN dpkg-reconfigure fontconfig-config && \
    dpkg-reconfigure fontconfig && \
    fc-cache -fv
