import connexion
import six
import time 

from flask import Response
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_resources import UserResources  # noqa: E501
from swagger_server import util
from swagger_server.controllers.user_info import UserInfo
from swagger_server.controllers.user_info import Users, print_users

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
    print("entering register_user")
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyUser = User.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyUser.user_id
        #TODO: check authToken
        print ("user_id = ", user_id)
        if user_id in Users:
            return Response("{'error message':'user already registered'}", status=409, mimetype='application/json')
        #TODO make data persistent
        #TODO: generate returned data
        timeStamp = time.time()
        print("timeStamp = ", timeStamp)
        nameSpace = user_id + str(timeStamp)
        #TODO: define the available Resources
        availableResources = {}
        user_resources = UserResources(nameSpace, availableResources)
        user_info = UserInfo(bodyUser, user_resources)
        Users[user_id] = user_info
        print("Users = ", str(Users))
        print_users()
        print("exiting register_user")
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
    print("entering unregister_user")
    try:
        if connexion.request.is_json:
            print ("inside if")
            body_json = connexion.request.get_json(force=True)
            print("body_json = ", str(body_json))
            bodyUser = User.from_dict(body_json)
            print("bodyUser = ", str(bodyUser))
            print ("exiting if")
        else:
            raise Exception('data payload is not json')
        # TODO check validity of parameters
        user_id = bodyUser.user_id
        #TODO: check authToken
        print ("user_id = ", user_id)
        #TODO verify the element exists
        # TODO cleanup all kinds of stuff
        if user_id in Users:
            print ("deleting user_id = ", user_id)
            del Users[user_id]
        else:
            return Response("{'error message':'user not registered'}", status=404, mimetype='application/json')
        print("Users = ", str(Users))
        print_users()
        print("exiting unregister_user")
        return
    except Exception as e:
        print("Exception: ", str(e))
        raise e
