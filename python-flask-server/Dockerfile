FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

# TODO: override via env vars
COPY conf.yaml /usr/src/app/

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server", "conf.yaml"]