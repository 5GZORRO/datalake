
import json
import s3_api

# Ingest is not a class method; it is a stand-alone function
def Ingest(args):
    # ingest_params is expected to be a str representing a json dictionary with the appropriate keys
    try:
        # verify structure of the data; create an exception if dictionary structure is not correct
        ingest_params = json.loads(args)
        operator_id = ingest_params['OperatorID']
        monitoring_data = ingest_params['MonitoringData']
        storage_location = ingest_params['StorageLocation']
        data_hash = ingest_params['DataHash']

        resoure_id = monitoring_data['resourceID']
        reference_id = monitoring_data['referenceID']
        metric_name = monitoring_data['metricName']
        metric_value = monitoring_data['metricValue']
        timestamp = monitoring_data['timestamp']
    except Exception as e:
         return 400

    # place the data in Object Store in specified location
    s3_proxy_server = s3_api.get_s3_proxy()
    s3_proxy_server.put_object(operator_id, storage_location, args, data_hash, timestamp, resoure_id)
    return 200

