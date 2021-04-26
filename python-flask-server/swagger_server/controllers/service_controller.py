import connexion
import six
import json

from swagger_server.models.create_service import CreateService  # noqa: E501
from swagger_server.models.get_service import GetService  # noqa: E501
from swagger_server.models.service_info import ServiceInfo  # noqa: E501
from swagger_server.models.service_metadata import ServiceMetadata  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
from swagger_server.controllers import user_info
from swagger_server.controllers import k8s_api

def prepare_deployment(container_def, service_id):
    deployment_template = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": service_id + "-deployment",
            "labels": {
                "app": service_id
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                  "app": service_id
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": service_id
	            }
                },
                "spec": {
                    "containers":  [ container_def ]
                }
            }
        }
    }
    return deployment_template

def prepare_service(container_def, service_id):
    print("entering prepare_service")
    service_template = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": service_id + "-service"
        },
        "spec": {
            "type": "NodePort",
            "selector": {
                "app": service_id
            },
            "ports": []
        }
    }

    # loop through the ports and create a service for each one
    ports = container_def['ports']
    print("ports = ", ports)
    for p in ports:
        entry = {"port": p["containerPort"]}
        if "name" in p:
            entry["name"] = p["name"]
        if "protocol" in p:
            entry["protocol"] = p["protocol"]
        service_template["spec"]["ports"].append(entry)

    print("exiting prepare_service")
    return service_template

def create_service(body):  # noqa: E501
    """Register a new service

     # noqa: E501

    :param body: Parameters to register service
    :type body: dict | bytes

    :rtype: ServiceMetadata
    """
    print("entering create_service")
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyService = CreateService.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyService.user_info.user_id
        #TODO: check authToken
        print ("user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')

        # TODO choose a better way to get a unique number
        service_id = user_id + '-service-' + str(user_info.next_index)
        user_info.next_index = user_info.next_index + 1

        user = user_info.get_user(user_id)
        container_def = bodyService.container_definition
        deployment_def = prepare_deployment(container_def, service_id)
        service_def = prepare_service(container_def, service_id)

        # load the service to k8s
        k8s_proxy_server = k8s_api.get_k8s_proxy()
        k8s_proxy_server.create_deployment(deployment_def)
        response = k8s_proxy_server.create_service(service_def)
        # TODO Fix this up and save all the service info in one proper place.
        # TODO extract the ip address of the service
        ports = response.spec.ports
        ports2 = str(ports)
        ports3 = json.loads(ports2.replace("'", '"'))
        service_metadata = ServiceMetadata(service_id, ports3)
        service_info = ServiceInfo(service_metadata, container_def)
        user.add_service(service_info)
        return service_metadata, 201
    except Exception as e:
        print("Exception: ", str(e))
        raise e

def delete_service_resources(s):
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    name = s.service_metadata.service_id + "-service"
    k8s_proxy_server.delete_service(name)
    name = s.service_metadata.service_id + "-deployment"
    k8s_proxy_server.delete_deployment(name)
    return

def delete_service():  # noqa: E501
    """Delete a service

     # noqa: E501

    :param body: Parameters to delete a service
    :type body: dict | bytes

    :rtype: None
    """
    print("entering delete_service")
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyService = GetService.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyService.user_info.user_id
        service_id = bodyService.service_id
        #TODO: check authToken
        print ("user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        services = user.serviceInfoList
        k8s_proxy_server = k8s_api.get_k8s_proxy()

        for s in services:
            if service_id == s.service_metadata.service_id:
                delete_service_resources(s)
                user.del_service(s)
                print("exiting delete_service")
                return
        return Response("{'error message':'service not found'}", status=404, mimetype='application/json')

    except Exception as e:
        print("Exception: ", str(e))
        raise e


def get_service():  # noqa: E501
    """Return details of specified service

     # noqa: E501

    :param body: Parameters to get a service
    :type body: dict | bytes

    :rtype: ServiceInfo
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyService = GetService.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyService.user_info.user_id
        service_id = bodyService.service_id
        #TODO: check authToken
        print ("get_service, user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        services = user.serviceInfoList

        for s in services:
            if service_id == s.service_metadata.service_id:
                return s, 200
        return Response("{'error message':'service not found'}", status=404, mimetype='application/json')

    except Exception as e:
        print("Exception: ", str(e))
        raise e


def list_services():  # noqa: E501
    """List all of the User&#39;s services

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[ServiceInfo]
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            u_info = User.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = u_info.user_id
        #TODO: check authToken
        print ("list_services, user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        services = user.serviceInfoList
        return services

    except Exception as e:
        print("Exception: ", str(e))
        raise e


