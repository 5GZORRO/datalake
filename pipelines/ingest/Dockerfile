
FROM python:3.6-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip3 install minio

ADD ingest.py /usr/src/app

CMD ["python", "ingest.py"]

