
FROM python:3.6-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip3 install minio

COPY . /usr/src/app

ENTRYPOINT ["python3"]

CMD ["__main__.py"]

