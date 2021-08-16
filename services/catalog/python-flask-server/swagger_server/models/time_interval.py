# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class TimeInterval(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, start_time: str=None, end_time: str=None):  # noqa: E501
        """TimeInterval - a model defined in Swagger

        :param start_time: The start_time of this TimeInterval.  # noqa: E501
        :type start_time: str
        :param end_time: The end_time of this TimeInterval.  # noqa: E501
        :type end_time: str
        """
        self.swagger_types = {
            'start_time': str,
            'end_time': str
        }

        self.attribute_map = {
            'start_time': 'startTime',
            'end_time': 'endTime'
        }

        self._start_time = start_time
        self._end_time = end_time

    @classmethod
    def from_dict(cls, dikt) -> 'TimeInterval':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TimeInterval of this TimeInterval.  # noqa: E501
        :rtype: TimeInterval
        """
        return util.deserialize_model(dikt, cls)

    @property
    def start_time(self) -> str:
        """Gets the start_time of this TimeInterval.


        :return: The start_time of this TimeInterval.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: str):
        """Sets the start_time of this TimeInterval.


        :param start_time: The start_time of this TimeInterval.
        :type start_time: str
        """

        self._start_time = start_time

    @property
    def end_time(self) -> str:
        """Gets the end_time of this TimeInterval.


        :return: The end_time of this TimeInterval.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: str):
        """Sets the end_time of this TimeInterval.


        :param end_time: The end_time of this TimeInterval.
        :type end_time: str
        """

        self._end_time = end_time
