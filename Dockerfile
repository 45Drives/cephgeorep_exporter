FROM python:3.9-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY cephgeorep_exporter.py /usr/src/app

ENTRYPOINT [ "python3", "-u", "./cephgeorep_exporter.py" ]
