#!/usr/bin/env python3

import json
import os
import io
import sys

from minio import Minio
from minio.error import S3Error

# Ingest is not a class method; it is a stand-alone function
def Ingest(data):
    # ingest_params is expected to be a str representing a json dictionary with the appropriate keys
    ingest_params = json.loads(data)
    operator_id = ingest_params['operatorID']
    transaction_id = ingest_params['transactionID']
    network_id = ingest_params['networkID']
    if 'monitoringData' in ingest_params:
        monitoring_data = ingest_params['monitoringData']
    elif 'MonitoringData' in ingest_params:
        monitoring_data = ingest_params['MonitoringData']
    else:
        raise("monitoringData field is missing")

    if 'instanceID' in monitoring_data:
        instance_id = monitoring_data['instanceID']
    elif 'instanceID' in ingest_params:
        instance_id = ingest_params['instanceID']
    else:
        raise("instanceID field is missing")

    if 'productID' in monitoring_data:
        product_id = monitoring_data['productID']
    elif 'ProductID' in monitoring_data:
        product_id = monitoring_data['ProductID']
    elif 'productID' in ingest_params:
        product_id = ingest_params['ProductID']
    elif 'ProductID' in ingest_params:
        product_id = ingest_params['ProductID']
    else:
        raise("productID field is missing")

    resource_id = monitoring_data['resourceID']
    metric_name = monitoring_data['metricName']
    metric_value = monitoring_data['metricValue']
    timestamp = monitoring_data['timestamp']
    reference_id = monitoring_data.get('referenceID', 'missing')

    # TODO: verify that bucket name is consistent with operator
    bucket_name = operator_id + "-dl-bucket"

    # place the data in Object Store in specified location
    s3_url = os.getenv('S3_URL', '127.0.0.1:9000')
    s3_access_key = os.getenv('S3_ACCESS_KEY', 'user')
    s3_secret_key = os.getenv('S3_SECRET_KEY', 'password')
    client = Minio(
        s3_url,
        access_key=s3_access_key,
        secret_key=s3_secret_key,
        secure=False,
    )

    object_name = resource_id + '/' + str(timestamp)
    found = client.bucket_exists(bucket_name)
    # convert data string into a bytes stream to be consumable by s3 client put_object.
    b = data.encode('utf-8')
    value_as_a_stream = io.BytesIO(b)
    if found:
        # TODO add hash as metadata to object
        rc = client.put_object(bucket_name, object_name, value_as_a_stream, len(data))

    output_params = {}
    output_params['resourceID'] = resource_id
    output_params['referenceID'] = reference_id
    output_params['transactionID'] = transaction_id
    output_params['productID'] = product_id
    output_params['instanceID'] = instance_id
    output_params['metricName'] = metric_name
    output_params['metricValue'] = metric_value
    output_params['timestamp'] = timestamp
    output_params['storageLocation'] = s3_url + '/' + bucket_name + '/' + object_name
    print(json.dumps(output_params))

def main():
    # extract paramters from argv[1]
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '{}'
    Ingest(args)



if __name__ == '__main__':
    main()

