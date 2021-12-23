
import os
import json

from swagger_server.controllers import service_controller
from swagger_server.controllers import k8s_api
from swagger_server.controllers import kafka_api

dl_catalaog_server_url = None
dl_catalog_server_name = "dl-catalog-server"
dl_stream_data_server_name = "dl-stream-data-server"
dl_stream_data_server_url = None
dl_stream_data_server_topic = "dl_stream_topic"

def create_dl_catalog_service():
    print("entering create_dl_catalog_service")
    k8s_proxy_server = k8s_api.get_k8s_proxy()

    postrges_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
    datalake_images_version = os.getenv('DATALAKE_IMAGES_VERSION', 'latest')
    container_def = {
        "name": dl_catalog_server_name,
        "image": "docker.pkg.github.com/5gzorro/datalake/dl_catalog_server:"+datalake_images_version,
        "imagePullSecrets": [
            { "name": "datalakeregistrykey" }
        ],
        "ports": [ {
            "name": "web",
            "containerPort": 8086,
            "protocol": "TCP",
        } ],
        "env": [
            { "name": "POSTGRES_HOST", "value": postrges_host }
        ]
    }
    deployment_def = service_controller.prepare_deployment(container_def, dl_catalog_server_name)
    k8s_proxy_server.create_deployment(deployment_def)
    service_def = service_controller.prepare_service(container_def, dl_catalog_server_name)
    response = k8s_proxy_server.create_service(service_def)
    ports1 = response.spec.ports
    ports2 = str(ports1)
    ports3 = ports2.replace("'", '"')
    ports4 = ports3.replace('None', '""')
    ports = json.loads(ports4)
    print("exiting create_dl_catalog_service")
    return ports

def create_dl_stream_data_service():
    print("entering create_dl_stream_data_service")
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    datalake_images_version = os.getenv('DATALAKE_IMAGES_VERSION', 'latest')
    kafka_url = os.getenv('KAFKA_URL', '127.0.0.1:9092')
    container_def = {
        "name": dl_stream_data_server_name,
        "image": "docker.pkg.github.com/5gzorro/datalake/stream_data:"+datalake_images_version,
        "imagePullSecrets": [
            { "name": "datalakeregistrykey" }
        ],
        "ports": [ {
            "name": "web",
            "containerPort": 8087,
            "protocol": "TCP",
        } ],
        "env": [
            { "name": "KAFKA_URL", "value": kafka_url },
            { "name": "KAFKA_TOPIC_IN", "value": dl_stream_data_server_topic }
        ]
    }
    deployment_def = service_controller.prepare_deployment(container_def, dl_stream_data_server_name)
    k8s_proxy_server.create_deployment(deployment_def)
    service_def = service_controller.prepare_service(container_def, dl_stream_data_server_name)
    response = k8s_proxy_server.create_service(service_def)
    ports1 = response.spec.ports
    ports2 = str(ports1)
    ports3 = ports2.replace("'", '"')
    ports4 = ports3.replace('None', '""')
    ports = json.loads(ports4)
    print("exiting create_dl_catalog_service")
    return ports

def setup_dl_catalog_service():
    print("entering setup_dl_catalog_service")
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    k8s_url = os.getenv('KUBERNETES_URL', '127.0.0.1:8443')
    k8s_host = k8s_url.split(':')[0]
    print("k8s_url = %s, k8s_host = %s" % (k8s_url, k8s_host))
    try:
        # see if the service already exists
        name = dl_catalog_server_name + "-service"
        response = k8s_proxy_server.read_service(name)
        ports1 = response[0].spec.ports
        ports2 = str(ports1)
        ports3 = ports2.replace("'", '"')
        ports4 = ports3.replace('None', '""')
        ports = json.loads(ports4)
    except Exception as e:
        print("did not find old dl-catalog-server service;")
        ports = create_dl_catalog_service()
    global dl_catalaog_server_url
    dl_catalaog_server_url = k8s_host + ":" + str(ports[0]['node_port'])
    print("dl_catalaog_server_url = ", dl_catalaog_server_url)
    print("exiting setup_dl_catalog_service")

def setup_dl_stream_data_service():
    print("entering setup_dl_stream_data_service")
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    k8s_url = os.getenv('KUBERNETES_URL', '127.0.0.1:8443')
    k8s_host = k8s_url.split(':')[0]
    try:
        # see if the service already exists
        name = dl_stream_data_server_name + "-service"
        response = k8s_proxy_server.read_service(name)
        ports1 = response[0].spec.ports
        ports2 = str(ports1)
        ports3 = ports2.replace("'", '"')
        ports4 = ports3.replace('None', '""')
        ports = json.loads(ports4)
    except Exception as e:
        print("did not find old dl-stream-data-server service;")
        ports = create_dl_stream_data_service()
    global dl_stream_data_server_url
    dl_stream_data_server_url = k8s_host + ":" + str(ports[0]['node_port'])
    print("dl_stream_data_server_url = ", dl_stream_data_server_url)
    print("exiting setup_dl_stream_data_service")

def create_global_services():
    setup_dl_catalog_service()
    setup_dl_stream_data_service()
