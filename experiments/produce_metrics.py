#!/usr/bin/env python3

import os
import sys
import yaml
import time
from json import dumps
from kafka import KafkaProducer

def get_monitoring_data(operator_id):
    print("entering send_monitoring_data")
    monitoring_data = {
            "resourceID": "resource1",
            "referenceID": "ref1",
            "transactionID": "tran1",
            "productID": "prod1",
            "instanceID": "inst1",
            "metricName": "metric1",
            "metricValue": "value1",
            "timestamp": 't'+str(time.time())
            }
    postMonitoringDataDict = {
            "operatorID": operator_id,
            "businessID": operator_id,
            "networkID": operator_id,
            "MonitoringData": monitoring_data,
            }
    print("postMonitoringDataDict = ", postMonitoringDataDict)

    return postMonitoringDataDict

def main():
    print("entering main")
    if len(sys.argv) < 3:
        print("Usage: python3 metrics_producer.py <operator_id> <kafka_topic>")
        raise Exception('incorrect number of command-line parameters')

    operator_id = sys.argv[1]
    kafka_topic = sys.argv[2]
    kafka_url = os.getenv('KAFKA_URL', '127.0.0.1:9092')
    print("kafka_url = ", kafka_url)
    print("kafka_topic = ", kafka_topic)
    producer = KafkaProducer(bootstrap_servers=[kafka_url],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

    while (True):
        data = get_monitoring_data(operator_id)
        rc = producer.send(kafka_topic, value=data)
        time.sleep(10)


if __name__ == '__main__':
    main()

