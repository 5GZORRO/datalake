import connexion
import six

from flask import Response
from swagger_server.models.create_pipeline import CreatePipeline  # noqa: E501
from swagger_server.models.get_pipeline import GetPipeline  # noqa: E501
from swagger_server.models.pipeline_info import PipelineInfo  # noqa: E501
from swagger_server.models.pipeline_metadata import PipelineMetadata  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

from swagger_server.controllers import user_info
from swagger_server.controllers import k8s_api
from swagger_server.controllers import kafka_api

def create_pipeline(body):  # noqa: E501
    """Register a new pipeline

     # noqa: E501

    :param body: Parameters to register pipeline
    :type body: dict | bytes

    :rtype: PipelineMetadata
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyPipeline = CreatePipeline.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyPipeline.user_info.user_id
        #TODO: check authToken
        print ("create_pipeline, user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        pipeline_def = bodyPipeline.pipeline_definition
        k8s_proxy_server = k8s_api.get_k8s_proxy()

        # load the argo workflow (pipeline) to k8s
        # TODO choose a better way to get a unique number
        event_source_name, kafka_key = k8s_proxy_server.create_eventsource(user_id, 'pipeline-in', user_info.next_index)
        print("event_source_name = ", event_source_name)
        user_info.next_index = user_info.next_index + 1
        response = k8s_proxy_server.create_sensor(event_source_name, kafka_key, pipeline_def)
        pipeline_id = response['metadata']['name']
        pipe_metadata = PipelineMetadata(pipeline_id, event_source_name)
        pipe_info = PipelineInfo(pipe_metadata, pipeline_def)
        user.add_pipeline(pipe_info, False)
        return pipe_metadata, 201
    except Exception as e:
        print("Exception: ", str(e))
        raise e

def delete_pipeline_resources(p):
    print("entering delete_pipeline_resources")
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    input_topic = p.pipeline_metadata.input_topic
    print("input_topic = ", input_topic)
    response = k8s_proxy_server.delete_sensor(p.pipeline_metadata.pipeline_id)
    k8s_proxy_server.delete_eventsource(input_topic)
    kafka_proxy_server = kafka_api.get_kafka_proxy()
    response = kafka_proxy_server.delete_topic(input_topic)
    return

def delete_pipeline():  # noqa: E501
    """Delete a pipeline

     # noqa: E501

    :param body: Parameters to delete a pipeline
    :type body: dict | bytes

    :rtype: None
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyPipeline = GetPipeline.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyPipeline.user_info.user_id
        pipeline_id = bodyPipeline.pipeline_id
        #TODO: check authToken
        print ("delete_pipeline, user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        pipelines = user.pipelineInfoList

        for p in pipelines:
            if pipeline_id == p.pipeline_metadata.pipeline_id:
                delete_pipeline_resources(p)
                user.del_pipeline(p, False)
                return
        return Response("{'error message':'pipeline not found'}", status=404, mimetype='application/json')

    except Exception as e:
        print("Exception: ", str(e))
        raise e


def get_pipeline():  # noqa: E501
    """Return details of specified pipeline

     # noqa: E501

    :param body: Parameters to get a pipeline
    :type body: dict | bytes

    :rtype: PipelineInfo
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            bodyPipeline = GetPipeline.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = bodyPipeline.user_info.user_id
        pipeline_id = bodyPipeline.pipeline_id
        #TODO: check authToken
        print ("get_pipeline, user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        pipelines = user.pipelineInfoList

        for p in pipelines:
            if pipeline_id == p.pipeline_metadata.pipeline_id:
                return p, 200
        return Response("{'error message':'pipeline not found'}", status=404, mimetype='application/json')

    except Exception as e:
        print("Exception: ", str(e))
        raise e


def list_pipelines():  # noqa: E501
    """List all of User&#39;s pipelines

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[PipelineInfo]
    """
    try:
        if connexion.request.is_json:
            body_json = connexion.request.get_json(force=True)
            u_info = User.from_dict(body_json)
        else:
            return Response("{'error message':'data is not in json format'}", status=400, mimetype='application/json')
        user_id = u_info.user_id
        #TODO: check authToken
        print ("list_pipelines, user_id = ", user_id)
        if not user_id in user_info.get_users():
            return Response("{'error message':'user not registered'}", status=400, mimetype='application/json')
        user = user_info.get_user(user_id)
        pipelines = user.pipelineInfoList
        return pipelines

    except Exception as e:
        print("Exception: ", str(e))
        raise e
