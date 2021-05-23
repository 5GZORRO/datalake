
import os
import json

from swagger_server.controllers import service_controller
from swagger_server.controllers import k8s_api

dl_catalaog_server_url = None

def create_dl_catalog_service():
    print("entering create_dl_catalog_service")
    dl_catalog_server_name = "dl-catalog-server"
    k8s_proxy_server = k8s_api.get_k8s_proxy()

    try:
        name = dl_catalog_server_name + "-service"
        k8s_proxy_server.delete_service(name)
    except Exception as e:
        print("could not delete old dl-catalog-server service", e)

    try:
        name = dl_catalog_server_name + "-deployment"
        k8s_proxy_server.delete_deployment(name)
    except Exception as e:
        print("could not delete old dl-catalog-server deployment", e)

    postrges_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
    # keep the nodePort identical across reincarnations of the service
    container_def = {
        "name": dl_catalog_server_name,
        "image": "dl_catalog_server",
        "ports": [ {
            "name": "web",
            "containerPort": 8086,
            "protocol": "TCP",
            "nodePort": 30852
        } ],
        "env": [
            { "name": "POSTGRES_HOST", "value": postrges_host }
        ],
        "imagePullPolicy": "Never"
    }
    deployment_def = service_controller.prepare_deployment(container_def, dl_catalog_server_name)
    k8s_proxy_server.create_deployment(deployment_def)
    service_def = service_controller.prepare_service(container_def, dl_catalog_server_name)
    response = k8s_proxy_server.create_service(service_def)
    ports = response.spec.ports
    ports2 = str(ports)
    ports3 = json.loads(ports2.replace("'", '"'))
    global dl_catalaog_server_url
    dl_catalaog_server_url = postrges_host + ":" + str(ports3[0]['node_port'])
    print("dl_catalaog_server_url = ", dl_catalaog_server_url)
    print("exiting create_dl_catalog_service")


def create_global_services():
    create_dl_catalog_service()
