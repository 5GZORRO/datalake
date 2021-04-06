import connexion
import six

from flask import Response
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_resources import UserResources  # noqa: E501
from swagger_server.models.pipeline_metadata import PipelineMetadata
from swagger_server.models.pipeline_info import PipelineInfo
from swagger_server import util
from swagger_server.controllers.user_info import UserInfo
from swagger_server.controllers import user_info
from swagger_server.controllers import k8s_api
from swagger_server.controllers import s3_api
from swagger_server.controllers import kafka_api
from swagger_server.controllers import pipeline_controller

def list_users():  # noqa: E501
    """List all User IDs

     # noqa: E501


    :rtype: List[str]
    """
    return list(user_info.Users)

def create_predefined_pipelines(user_id):
    print("entering create_predefined_pipelines")
    # create default ingest metrics pipeline
    # TODO: Fix the URLs of the parameters
    # TODO: Do not return the secrets to the user!!!
    ingest_def = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Workflow",
        "metadata": {
            "generateName": "ingest-"
        },
        "spec": {
            "entrypoint": "ingest",
            "arguments": {
                "parameters": [ {
                    "name": "args",
                    "value": "my args"
                } ]
            },
            "templates": [ {
                "name": "ingest",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                } ]
                },
                "container": {
                    "image": "ingest",
            "env": [
                { "name": "S3_URL",
                "value": "192.168.122.176:9000" },
                { "name": "S3_ACCESS_KEY",
                "value": "user" },
                { "name": "S3_SECRET_KEY",
                "value": "password" }
            ],
            "imagePullPolicy": "Never",
                    "command": [ "python", "./__main__.py" ],
                    "args": ["{{inputs.parameters.args}}"],
                    "resources": {
                        "limits": {
                            "memory": "32Mi",
                            "cpu": "100m"
                        }
                    }
                }
            } ]
        }
    }
    # TODO: fix parameters
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    ingest_topic, kafka_key = k8s_proxy_server.create_eventsource(user_id, 'in', pipeline_number=0)
    response = k8s_proxy_server.create_sensor(ingest_topic, kafka_key, ingest_def)
    pipeline_id = response['metadata']['name']
    output_topic = ''
    pipe_metadata = PipelineMetadata(pipeline_id, ingest_topic, output_topic)
    pipe_info = PipelineInfo(pipe_metadata, ingest_def)
    pipeline_topics = { "resourceMetricsIngestPipeline" : ingest_topic }
    predefined_pipes = list()
    predefined_pipes.append(pipe_info)

    # Add here additional pipelines, as needed

    print(pipeline_topics)
    print("exiting create_predefined_pipelines")
    return pipeline_topics, predefined_pipes

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
        if user_id in user_info.Users:
            return Response("{'error message':'user already registered'}", status=409, mimetype='application/json')

        #TODO make data persistent

        # generate returned data
        nameSpace = user_id

        #TODO: define the available Resources
        k8s_proxy_server = k8s_api.get_k8s_proxy()
        s3_proxy_server = s3_api.get_s3_proxy()
        kafka_proxy_server = kafka_api.get_kafka_proxy()
        # TODO change this to a function call
        s3_bucket_name = s3_proxy_server.create_bucket(user_id, "dl-bucket")
        urls = {}
        urls['k8s_url'] = k8s_proxy_server.k8s_url
        urls['kafka_url'] = kafka_proxy_server.kafka_url
        urls['s3_url'] = s3_proxy_server.s3_url
        # create general kafka topics for the user to use
        topic_name_in = user_id + "-topic-in"
        topic_name_out = user_id + "-topic-out"
        kafka_proxy_server.create_topic(user_id, topic_name_in)
        kafka_proxy_server.create_topic(user_id, topic_name_out)
        topics = {
                "userInTopic": topic_name_in,
                "userOutTopic": topic_name_out,
                }
        pipeline_topics, predefined_pipes = create_predefined_pipelines(user_id)
        print(pipeline_topics)
        print(predefined_pipes)
        # TODO: make variable names consistent
        availableResources = {
                "pipelines": pipeline_topics,
                "topics": topics,
                "urls": urls,
                "s3_bucket": s3_bucket_name,
                }
        user_resources = UserResources(nameSpace, availableResources)
        u_info = UserInfo(bodyUser, user_resources, predefined_pipes)
        user_info.Users[user_id] = u_info

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
        if user_id in user_info.Users:
            user = user_info.Users[user_id]
        else:
            return Response("{'error message':'user not registered'}", status=404, mimetype='application/json')
        # TODO cleanup all kinds of stuff
        kafka_proxy_server = kafka_api.get_kafka_proxy()
        kafka_proxy_server.delete_topic(user.userResources.available_resources["topics"]["userInTopic"])
        kafka_proxy_server.delete_topic(user.userResources.available_resources["topics"]["userOutTopic"])

        # TODO verify the bucket is empty - or empty it out
        #s3_proxy_server = s3_api.get_s3_proxy()
        #s3_proxy_server.delete_bucket(user.userResources.available_resources["s3_bucket"])

        # delete all pipelines:
        k8s_proxy_server = k8s_api.get_k8s_proxy()
        pipelines = user.pipelineInfoList
        print(pipelines)
        while len(pipelines) > 0:
            p = pipelines[0]
            # TODO: delete kafka topics, etc
            # TODO: ignore exceptions that occur here, and continue to clean up
            pipeline_controller.delete_pipeline_resources(p)
            pipelines.remove(p)

        pipelines = user.predefinedPipes
        print(pipelines)
        while len(pipelines) > 0:
            p = pipelines[0]
            # TODO: delete kafka topics, etc
            # TODO: ignore exceptions that occur here, and continue to clean up
            pipeline_controller.delete_pipeline_resources(p)
            pipelines.remove(p)

        print ("deleting user_id = ", user_id)
        del user_info.Users[user_id]
        return
    except Exception as e:
        print("Exception: ", str(e))
        raise e
