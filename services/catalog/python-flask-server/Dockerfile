FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install psycopg2-binary

RUN pip install connexion[swagger-ui]

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt


COPY . /usr/src/app

EXPOSE 8086

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
