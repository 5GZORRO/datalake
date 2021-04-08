# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.create_service import CreateService  # noqa: E501
from swagger_server.models.get_service import GetService  # noqa: E501
from swagger_server.models.service_info import ServiceInfo  # noqa: E501
from swagger_server.models.service_metadata import ServiceMetadata  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServiceController(BaseTestCase):
    """ServiceController integration test stubs"""

    def test_create_service(self):
        """Test case for create_service

        Register a new pipeline
        """
        body = CreateService()
        response = self.client.open(
            '/datalake/v1/service',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_service(self):
        """Test case for delete_service

        Delete a service
        """
        body = GetService()
        response = self.client.open(
            '/datalake/v1/service',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_service(self):
        """Test case for get_service

        Return details of specified service
        """
        body = GetService()
        response = self.client.open(
            '/datalake/v1/service',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_services(self):
        """Test case for list_services

        List all of the User's services
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/service/all',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
