export KAFKA_TOPIC=dl_stream_topic
python3 copy_to_topic.py '{"operatorID": "user1", "networkID": "net1", "transactionID": "tran1", "monitoringData": {"resourceID": "resource1", "productID": "prod1", "instanceID": "inst1", "metricName": "metric1", "metricValue": "value1", "timestamp": "t1620651855.1799903"}, "StorageLocation": "user1-dl-bucket", "DataHash": "blah"}'
