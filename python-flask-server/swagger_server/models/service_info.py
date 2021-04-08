# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util
from swagger_server.models.service_metadata import ServiceMetadata


class ServiceInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, service_metadata: ServiceMetadata=None, deployment_definition: object=None, service_definition: object=None):  # noqa: E501
        """ServiceInfo - a model defined in Swagger

        :param service_metadata: The service_metadata of this ServiceInfo.  # noqa: E501
        :type service_metadata: ServiceMetadata
        :param deployment_definition: The deployment_definition of this ServiceInfo.  # noqa: E501
        :type deployment_definition: object
        :param service_definition: The service_definition of this ServiceInfo.  # noqa: E501
        :type service_definition: object
        """
        self.swagger_types = {
            'service_metadata': ServiceMetadata,
            'deployment_definition': object,
            'service_definition': object
        }

        self.attribute_map = {
            'service_metadata': 'serviceMetadata',
            'deployment_definition': 'deploymentDefinition',
            'service_definition': 'serviceDefinition'
        }

        self._service_metadata = service_metadata
        self._deployment_definition = deployment_definition
        self._service_definition = service_definition

    @classmethod
    def from_dict(cls, dikt) -> 'ServiceInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ServiceInfo of this ServiceInfo.  # noqa: E501
        :rtype: ServiceInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def service_metadata(self) -> ServiceMetadata:
        """Gets the service_metadata of this ServiceInfo.


        :return: The service_metadata of this ServiceInfo.
        :rtype: ServiceMetadata
        """
        return self._service_metadata

    @service_metadata.setter
    def service_metadata(self, service_metadata: ServiceMetadata):
        """Sets the service_metadata of this ServiceInfo.


        :param service_metadata: The service_metadata of this ServiceInfo.
        :type service_metadata: ServiceMetadata
        """

        self._service_metadata = service_metadata

    @property
    def deployment_definition(self) -> object:
        """Gets the deployment_definition of this ServiceInfo.


        :return: The deployment_definition of this ServiceInfo.
        :rtype: object
        """
        return self._deployment_definition

    @deployment_definition.setter
    def deployment_definition(self, deployment_definition: object):
        """Sets the deployment_definition of this ServiceInfo.


        :param deployment_definition: The deployment_definition of this ServiceInfo.
        :type deployment_definition: object
        """

        self._deployment_definition = deployment_definition

    @property
    def service_definition(self) -> object:
        """Gets the service_definition of this ServiceInfo.


        :return: The service_definition of this ServiceInfo.
        :rtype: object
        """
        return self._service_definition

    @service_definition.setter
    def service_definition(self, service_definition: object):
        """Sets the service_definition of this ServiceInfo.


        :param service_definition: The service_definition of this ServiceInfo.
        :type service_definition: object
        """

        self._service_definition = service_definition
