FROM python:3

ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./start /start
RUN chmod +x /start
COPY ./udpserver /udpserver

WORKDIR /
