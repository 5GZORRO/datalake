# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.product_query import ProductQuery  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProductController(BaseTestCase):
    """ProductController integration test stubs"""

    def test_register_product_topic(self):
        """Test case for register_product_topic

        register productId for which data should be streamed
        """
        body = ProductQuery()
        response = self.client.open(
            '/datalake/v1/stream_data/register/{productId}'.format(productId='productId_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_unregister_product_topic(self):
        """Test case for unregister_product_topic

        stop stream data for specified  productId
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/stream_data/unregister/{productId}'.format(productId='productId_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
