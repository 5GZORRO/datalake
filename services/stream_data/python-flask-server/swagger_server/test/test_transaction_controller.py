# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.transaction_query import TransactionQuery  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTransactionController(BaseTestCase):
    """TransactionController integration test stubs"""

    def test_register_transaction_topic(self):
        """Test case for register_transaction_topic

        register transactionId for which data should be streamed
        """
        body = TransactionQuery()
        response = self.client.open(
            '/datalake/v1/stream_data/register/{transactionId}'.format(transactionId='transactionId_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_unregister_transaction_topic(self):
        """Test case for unregister_transaction_topic

        stop stream data for specified  transactionId
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/stream_data/unregister/{transactionId}'.format(transactionId='transactionId_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
