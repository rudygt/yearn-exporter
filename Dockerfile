FROM python:3.6-buster

RUN pip3 install eth-brownie prometheus_client dataclasses
RUN mkdir -p /app/yearn-exporter
ADD . /app/yearn-exporter
WORKDIR /app/yearn-exporter

ENTRYPOINT ["./entrypoint.sh"]
