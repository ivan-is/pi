FROM python:3.8-slim

WORKDIR /app

RUN set -x && pip3 install -U pip && pip3 install requests==2.25.1

ADD pistats/manage.py /app/manage.py

EXPOSE 8000

ENV RPI_MONITOR_ROUTE='http://rpi-monitor:8888/dynamic.json'
ENV KERNEL_RELEASE='5.10.17-v7l+'

CMD python3 -m manage 8000
