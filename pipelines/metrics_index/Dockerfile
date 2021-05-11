
FROM python:3

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip install psycopg2-binary

ADD metrics_index.py /usr/src/app

CMD ["python", "/usr/src/app/metrics_index.py"]

