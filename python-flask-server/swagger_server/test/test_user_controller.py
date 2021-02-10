# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_resources import UserResources  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_list_users(self):
        """Test case for list_users

        List all User IDs
        """
        response = self.client.open(
            '/datalake/v1/user/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_user(self):
        """Test case for register_user

        Register a new user
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/user',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_unregister_user(self):
        """Test case for unregister_user

        Unregister a user
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/user',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
