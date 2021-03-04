#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.controllers.k8s_api import K8s_Proxy, set_k8s_proxy
from swagger_server.controllers.s3_api import S3_Proxy, set_s3_proxy
from swagger_server.controllers.kafka_api import Kafka_Proxy, set_kafka_proxy


def main():
    print("entering main")
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Data Lake API'})
    k8s_proxy = K8s_Proxy()
    set_k8s_proxy(k8s_proxy)
    s3_proxy = S3_Proxy()
    set_s3_proxy(s3_proxy)
    kafka_proxy = Kafka_Proxy()
    set_kafka_proxy(kafka_proxy)
    app.run(port=8080)


if __name__ == '__main__':
    main()
