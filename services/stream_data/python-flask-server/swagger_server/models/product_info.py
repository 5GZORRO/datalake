# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ProductInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, topic: str=None):  # noqa: E501
        """ProductInfo - a model defined in Swagger

        :param topic: The topic of this ProductInfo.  # noqa: E501
        :type topic: str
        """
        self.swagger_types = {
            'topic': str
        }

        self.attribute_map = {
            'topic': 'topic'
        }

        self._topic = topic

    @classmethod
    def from_dict(cls, dikt) -> 'ProductInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ProductInfo of this ProductInfo.  # noqa: E501
        :rtype: ProductInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def topic(self) -> str:
        """Gets the topic of this ProductInfo.


        :return: The topic of this ProductInfo.
        :rtype: str
        """
        return self._topic

    @topic.setter
    def topic(self, topic: str):
        """Sets the topic of this ProductInfo.


        :param topic: The topic of this ProductInfo.
        :type topic: str
        """

        self._topic = topic
