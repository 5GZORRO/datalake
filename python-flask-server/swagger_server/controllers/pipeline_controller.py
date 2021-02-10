import connexion
import six

from swagger_server.models.create_pipeline import CreatePipeline  # noqa: E501
from swagger_server.models.get_pipeline import GetPipeline  # noqa: E501
from swagger_server.models.pipeline_info import PipelineInfo  # noqa: E501
from swagger_server.models.pipeline_metadata import PipelineMetadata  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def create_pipeline(body):  # noqa: E501
    """Register a new pipeline

     # noqa: E501

    :param body: Parameters to register pipeline
    :type body: dict | bytes

    :rtype: PipelineMetadata
    """
    if connexion.request.is_json:
        body = CreatePipeline.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_pipeline(body):  # noqa: E501
    """Delete a pipeline

     # noqa: E501

    :param body: Parameters to delete a pipeline
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = GetPipeline.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_pipeline(body):  # noqa: E501
    """Return details of specified pipeline

     # noqa: E501

    :param body: Parameters to get a pipeline
    :type body: dict | bytes

    :rtype: PipelineInfo
    """
    if connexion.request.is_json:
        body = GetPipeline.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def list_pipelines(body):  # noqa: E501
    """List all of User&#39;s pipelines

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[PipelineInfo]
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
