
FROM python:3.6-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip3 install kafka-python

ADD copy_to_topic.py /usr/src/app

CMD ["python", "copy_to_topic.py"]

