
import os
import json

from swagger_server.controllers import service_controller
from swagger_server.controllers import k8s_api

dl_catalaog_server_url = None
dl_catalog_server_name = "dl-catalog-server"

def create_dl_catalog_service():
    print("entering create_dl_catalog_service")
    k8s_proxy_server = k8s_api.get_k8s_proxy()

    postrges_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
    container_def = {
        "name": dl_catalog_server_name,
        "image": "docker.pkg.github.com/5gzorro/datalake/dl_catalog_server",
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
    ports = json.loads(ports2.replace("'", '"'))
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
        ports = json.loads(ports2.replace("'", '"'))
    except Exception as e:
        print("did not find old dl-catalog-server service;")
        ports = create_dl_catalog_service()
    global dl_catalaog_server_url
    dl_catalaog_server_url = k8s_host + ":" + str(ports[0]['node_port'])
    print("dl_catalaog_server_url = ", dl_catalaog_server_url)
    print("esiting setup_dl_catalog_service")


def create_global_services():
    setup_dl_catalog_service()
