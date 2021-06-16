import connexion
import six
import os

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
from swagger_server.controllers import service_controller
from swagger_server.controllers import dl_global_services

def get_user():  # noqa: E501
    """Get user availableResources

     # noqa: E501

    :param body: Parameters to get User info from the Data Lake
    :type body: dict | bytes

    :rtype: UserResources
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
        print ("get_user, user_id = ", user_id)
        # verify the element exists
        if user_id in user_info.get_users():
            user = user_info.get_user(user_id)
        else:
            return Response("{'error message':'user not registered'}", status=404, mimetype='application/json')
        user_resources = user.userResources
        return user_resources, 201
    except Exception as e:
        print("Exception: ", str(e))
        raise e

def list_users():  # noqa: E501
    """List all User IDs

     # noqa: E501


    :rtype: List[str]
    """
    return list(user_info.get_users())

#TODO separate this out into a separate file
def create_predefined_pipelines(user_id, s3_available : bool):
    print("entering create_predefined_pipelines")
    predefined_pipes = list()
    pipeline_topics = { }
    if not s3_available:
        return pipeline_topics, predefined_pipes
    # create default ingest metrics pipeline
    # TODO: perhaps move this to a config file yaml and have a more general mechanism to add predefined pipelines
    datalake_images_version = os.getenv('DATALAKE_IMAGES_VERSION', '1.0')
    ingest_def = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Workflow",
        "metadata": {
            "generateName": "ingest-pipeline-"
        },
        "spec": {
            "entrypoint": "ingest-and-index",
            "imagePullSecrets": [
                { "name": "datalakeregistrykey" }
            ],
            "arguments": {
                "parameters": [ {
                    "name": "args",
                    "value": "my args"
                } ]
            },
            "templates": [
              {
                "name": "ingest-and-index",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "steps": [
                    [ {
                        "name": "ingest1",
                        "template": "ingest",
                        "arguments": {
                            "parameters": [ {
                                "name": "args",
                                "value": "{{inputs.parameters.args}}"
                            } ]
                        }
                    } ],
                    [ {
                        "name": "index1",
                        "template": "metrics-index",
                        "arguments": {
                            "parameters": [ {
                                "name": "args",
                                "value": "{{steps.ingest1.outputs.result}}"
                            } ]
                        }
                    } ]
                ]
              },
              {
                "name": "ingest",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "container": {
                    "image": "docker.pkg.github.com/5gzorro/datalake/ingest:"+datalake_images_version,
                    "env": [
                        { "name": "S3_URL",
                        "value": os.getenv('S3_URL', '127.0.0.1:9000') },
                        { "name": "S3_ACCESS_KEY",
                        "value": os.getenv('S3_ACCESS_KEY', 'user') },
                        { "name": "S3_SECRET_KEY",
                        "value": os.getenv('S3_SECRET_KEY', 'password') },
                    ],
                    "command": [ "python", "./ingest.py" ],
                    "args": ["{{inputs.parameters.args}}"],
                    "resources": {
                        "limits": {
                            "memory": "32Mi",
                            "cpu": "100m"
                        }
                    }
                }
              },
              {
                "name": "metrics-index",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "container": {
                    "image": "docker.pkg.github.com/5gzorro/datalake/metrics_index:"+datalake_images_version,
                    "env": [
                        { "name": "POSTGRES_HOST",
                        "value": os.getenv("POSTGRES_HOST", "127.0.0.1") },
                    ],
                    "command": [ "python", "./metrics_index.py" ],
                    "args": ["{{inputs.parameters.args}}"],
                    "resources": {
                        "limits": {
                            "memory": "32Mi",
                            "cpu": "100m"
                        }
                    }
                }
              }
            ]
        }
    }
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    try:
        ingest_topic, kafka_key = k8s_proxy_server.create_eventsource(user_id, 'in', pipeline_number=0)
        print("ingest_topic = ", ingest_topic)
        response = k8s_proxy_server.create_sensor(ingest_topic, kafka_key, ingest_def)
        pipeline_id = response['metadata']['name']
        pipe_metadata = PipelineMetadata(pipeline_id, ingest_topic)
        pipe_info = PipelineInfo(pipe_metadata, ingest_def)
        pipeline_topics["resourceMetricsIngestPipeline"] = ingest_topic
        predefined_pipes.append(pipe_info)
    except Exception as e:
        print("Exception: ", str(e))

    # Add here additional pipelines, as needed

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
        if user_id in user_info.get_users():
            return Response("{'error message':'user already registered'}", status=409, mimetype='application/json')

        # generate returned data
        nameSpace = user_id
        k8s_proxy_server = k8s_api.get_k8s_proxy()
        s3_proxy_server = s3_api.get_s3_proxy()
        kafka_proxy_server = kafka_api.get_kafka_proxy()
        s3_bucket_name = s3_proxy_server.create_bucket(user_id, "dl-bucket")
        urls = {}
        urls['k8s_url'] = k8s_proxy_server.k8s_url
        urls['kafka_url'] = kafka_proxy_server.kafka_url
        if s3_bucket_name:
            urls['s3_url'] = s3_proxy_server.s3_url
        urls['dl_catalog_server_url'] = dl_global_services.dl_catalaog_server_url

        # create general kafka topics for the user to use
        topic_name_in = user_id + "-topic-in"
        topic_name_out = user_id + "-topic-out"
        kafka_proxy_server.create_topic(user_id, topic_name_in)
        kafka_proxy_server.create_topic(user_id, topic_name_out)
        topics = {
                "userInTopic": topic_name_in,
                "userOutTopic": topic_name_out,
                }
        pipeline_topics, predefined_pipes = create_predefined_pipelines(user_id, s3_bucket_name != None)
        # TODO: make variable names consistent
        availableResources = {
                "pipelines": pipeline_topics,
                "topics": topics,
                "urls": urls
                }
        if s3_bucket_name:
            availableResources["s3_bucket"] = s3_bucket_name
        user_resources = UserResources(nameSpace, availableResources)
        u_info = UserInfo(bodyUser, user_resources)

        user_info.add_user(user_id, u_info)

        # only after the user_info exists can we register with it the predefined pipes
        for p in predefined_pipes:
            u_info.add_pipeline(p, True)

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
        if user_id in user_info.get_users():
            user = user_info.get_user(user_id)
        else:
            return Response("{'error message':'user not registered'}", status=404, mimetype='application/json')
        # cleanup all kinds of stuff
        kafka_proxy_server = kafka_api.get_kafka_proxy()
        kafka_proxy_server.delete_topic(user.userResources.available_resources["topics"]["userInTopic"])
        kafka_proxy_server.delete_topic(user.userResources.available_resources["topics"]["userOutTopic"])

        # TODO verify the bucket is empty - or empty it out
        #s3_proxy_server = s3_api.get_s3_proxy()
        #s3_proxy_server.delete_bucket(user.userResources.available_resources["s3_bucket"])

        # delete all pipelines:
        # use deep copy of the list of pipes, since the original list of pipes will be updated inside the loop
        pipelines = user.predefinedPipes.copy()
        for p in pipelines:
            pipeline_controller.delete_pipeline_resources(p)
            user.del_pipeline(p, True)

        pipelines = user.pipelineInfoList.copy()
        for p in pipelines:
            pipeline_controller.delete_pipeline_resources(p)
            user.del_pipeline(p, False)

        # delete all services:
        services = user.serviceInfoList.copy()
        for s in services:
            service_controller.delete_service_resources(s)
            user.del_service(s)

        print ("deleting user_id = ", user_id)
        user_info.del_user(user_id)
        return
    except Exception as e:
        print("Exception: ", str(e))
        raise e
