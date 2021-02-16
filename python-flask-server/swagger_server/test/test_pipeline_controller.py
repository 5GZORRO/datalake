# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.create_pipeline import CreatePipeline  # noqa: E501
from swagger_server.models.get_pipeline import GetPipeline  # noqa: E501
from swagger_server.models.pipeline_info import PipelineInfo  # noqa: E501
from swagger_server.models.pipeline_metadata import PipelineMetadata  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPipelineController(BaseTestCase):
    """PipelineController integration test stubs"""

    def test_create_pipeline(self):
        """Test case for create_pipeline

        Register a new pipeline
        """
        body = CreatePipeline()
        response = self.client.open(
            '/datalake/v1/pipeline',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_pipeline(self):
        """Test case for delete_pipeline

        Delete a pipeline
        """
        body = GetPipeline()
        response = self.client.open(
            '/datalake/v1/pipeline',
            method='DELETE',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_pipeline(self):
        """Test case for get_pipeline

        Return details of specified pipeline
        """
        body = GetPipeline()
        response = self.client.open(
            '/datalake/v1/pipeline',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_pipelines(self):
        """Test case for list_pipelines

        List all of the User's pipelines
        """
        body = User()
        response = self.client.open(
            '/datalake/v1/pipeline/all',
            method='GET',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
