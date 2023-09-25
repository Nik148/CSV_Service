FROM debian:latest

RUN apt-get update && \
    apt-get install -y python3

RUN apt-get -y install python3-pip

COPY ./ .

RUN apt-get -y install virtualenv && virtualenv venv

RUN . /venv/bin/activate && pip3 install -r /requirements.txt