# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.resource_entries_info import ResourceEntriesInfo  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestResourceController(BaseTestCase):
    """ResourceController integration test stubs"""

    def test_get_resource(self):
        """Test case for get_resource

        Return entries related to specified resource
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/catalog/resource/{resourceId}'.format(resourceId='resourceId_example'),
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
