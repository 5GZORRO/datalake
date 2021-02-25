import connexion
import six

from flask import Response
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_resources import UserResources  # noqa: E501
from swagger_server import util
from swagger_server.controllers.user_info import UserInfo
from swagger_server.controllers.user_info import Users, print_users
from swagger_server.controllers.k8s_api import get_k8s_proxy
from swagger_server.controllers.pipeline_controller import delete_pipeline_resources

def list_users():  # noqa: E501
    """List all User IDs

     # noqa: E501


    :rtype: List[str]
    """
    return list(Users)


def register_user(body):  # noqa: E501
    """Register a new user

     # noqa: E501

    :param body: Parameters to register User that is connecting to the services of the Data Lake
    :type body: dict | bytes

    :rtype: UserResources
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyUser = User.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyUser.user_id
        #TODO: check authToken
        print ("register_user, user_id = ", user_id)
        if user_id in Users:
            return Response("{'error message':'user already registered'}", status=409, mimetype='application/json')

        #TODO make data persistent
        #TODO: generate returned data
        nameSpace = user_id

        #TODO: define the available Resources
        k8s_proxy_server = get_k8s_proxy()
        pipelines = {}
        topics = {}
        urls = k8s_proxy_server.conf_info
        availableResources = {
                "pipelines": pipelines,
                "topics": topics,
                "urls": urls
                }
        user_resources = UserResources(nameSpace, availableResources)
        user_info = UserInfo(bodyUser, user_resources)
        Users[user_id] = user_info
        print_users()
        return user_resources, 201
    except Exception as e:
        print("Exception: ", str(e))
        raise e



#def unregister_user(body):  # noqa: E501
def unregister_user():  # noqa: E501
    """Unregister a user

     # noqa: E501

    :param body: Parameters to unregister User from the Data Lake
    :type body: dict | bytes

    :rtype: None
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyUser = User.from_dict(body_json)
        else:
            raise Exception('data payload is not json')
        # TODO check validity of parameters
        user_id = bodyUser.user_id
        #TODO: check authToken
        print ("unregister_user, user_id = ", user_id)
        # verify the element exists
        if user_id in Users:
            user = Users[user_id]
        else:
            return Response("{'error message':'user not registered'}", status=404, mimetype='application/json')
        # TODO cleanup all kinds of stuff

        # delete all pipelines:
        k8s_proxy_server = get_k8s_proxy()
        pipelines = user.pipelineInfoList
        while len(pipelines) > 0:
            p = pipelines[0]
            print("deleting pipeline: ", p)
            # TODO: delete kafka topics, etc
            # TODO: ignore exceptions that occur here, and continue to clean up
            delete_pipeline_resources(p)
            pipelines.remove(p)
            print_users()

        print ("deleting user_id = ", user_id)
        del Users[user_id]
        print_users()
        return
    except Exception as e:
        print("Exception: ", str(e))
        raise e
