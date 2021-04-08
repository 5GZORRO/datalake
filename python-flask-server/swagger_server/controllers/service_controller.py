import connexion
import six

from swagger_server.models.create_service import CreateService  # noqa: E501
from swagger_server.models.get_service import GetService  # noqa: E501
from swagger_server.models.service_info import ServiceInfo  # noqa: E501
from swagger_server.models.service_metadata import ServiceMetadata  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
from swagger_server.controllers import user_info
from swagger_server.controllers import k8s_api

next_index = 101

def create_service(body):  # noqa: E501
    """Register a new service

     # noqa: E501

    :param body: Parameters to register service
    :type body: dict | bytes

    :rtype: ServiceMetadata
    """
    print("entering create_service")
    print("Users = ", str(user_info.Users))
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyService = CreateService.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyService.user_info.user_id
        #TODO: check authToken
        print ("user_id = ", user_id)
        if not user_id in user_info.Users:
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.Users[user_id]
        deployment_def = bodyService.deployment_definition
        service_def = bodyService.service_definition
        k8s_proxy_server = k8s_api.get_k8s_proxy()

        # load the service to k8s
        # TODO choose a better way to get a unique number
        global next_index
        #response = k8s_proxy_server.create_service(user_id, next_index, deployment_def, service_def)
        #service_id = response['metadata']['name']
        service_id = k8s_proxy_server.create_service(user_id, next_index, deployment_def, service_def)
        next_index = next_index + 1
        # TODO extract the ip address of the service
        ip_addr = "127.0.0.1"
        service_metadata = ServiceMetadata(service_id, ip_addr)
        service_info = ServiceInfo(service_metadata, deployment_def, service_def)
        user.serviceInfoList.append(service_info)
        print("exiting create_service")
        return service_metadata, 201
    except Exception as e:
        print("Exception: ", str(e))
        raise e

def delete_service_resources(s):
    print("entering delete_service_resources")
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    response = k8s_proxy_server.delete_service(s.service_metadata.service_id)
    print("response = ", response)
    print("exiting delete_service_resources")
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
        if not user_id in user_info.Users:
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.Users[user_id]
        services = user.serviceInfoList
        k8s_proxy_server = k8s_api.get_k8s_proxy()

        for s in services:
            if service_id == s.service_metadata.service_id:
                delete_service_resources(s)
                services.remove(s)
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
        if not user_id in user_info.Users:
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.Users[user_id]
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
        if not user_id in user_info.Users:
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.Users[user_id]
        services = user.serviceInfoList
        return services

    except Exception as e:
        print("Exception: ", str(e))
        raise e

