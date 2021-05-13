
FROM python:3.6-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip3 install kafka-python

COPY . /usr/src/app

ENTRYPOINT ["python3"]

CMD ["copy_data.py"]

