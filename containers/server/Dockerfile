FROM node:8

RUN apt-get update
RUN apt-get install -y libsndfile1
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

RUN pip3 install numpy scipy soundfile wavio