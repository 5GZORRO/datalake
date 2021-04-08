# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PipelineMetadata(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, pipeline_id: str=None, input_topic: str=None):  # noqa: E501
        """PipelineMetadata - a model defined in Swagger

        :param pipeline_id: The pipeline_id of this PipelineMetadata.  # noqa: E501
        :type pipeline_id: str
        :param input_topic: The input_topic of this PipelineMetadata.  # noqa: E501
        :type input_topic: str
        """
        self.swagger_types = {
            'pipeline_id': str,
            'input_topic': str
        }

        self.attribute_map = {
            'pipeline_id': 'pipelineId',
            'input_topic': 'inputTopic'
        }

        self._pipeline_id = pipeline_id
        self._input_topic = input_topic

    @classmethod
    def from_dict(cls, dikt) -> 'PipelineMetadata':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PipelineMetadata of this PipelineMetadata.  # noqa: E501
        :rtype: PipelineMetadata
        """
        return util.deserialize_model(dikt, cls)

    @property
    def pipeline_id(self) -> str:
        """Gets the pipeline_id of this PipelineMetadata.


        :return: The pipeline_id of this PipelineMetadata.
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id: str):
        """Sets the pipeline_id of this PipelineMetadata.


        :param pipeline_id: The pipeline_id of this PipelineMetadata.
        :type pipeline_id: str
        """

        self._pipeline_id = pipeline_id

    @property
    def input_topic(self) -> str:
        """Gets the input_topic of this PipelineMetadata.


        :return: The input_topic of this PipelineMetadata.
        :rtype: str
        """
        return self._input_topic

    @input_topic.setter
    def input_topic(self, input_topic: str):
        """Sets the input_topic of this PipelineMetadata.


        :param input_topic: The input_topic of this PipelineMetadata.
        :type input_topic: str
        """

        self._input_topic = input_topic
