import os
import connexion
import json
import six
import threading

from flask import Response
from kafka import KafkaConsumer, KafkaProducer

from swagger_server.models.transaction_query import TransactionQuery  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

kafka_url = None
kafka_topic_in = None

mapping_table = dict()

def handle_stream_data():
    consumer = KafkaConsumer(
            kafka_topic_in,
            bootstrap_servers=[kafka_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group')

    producer = KafkaProducer(
            bootstrap_servers=[kafka_url],
            value_serializer=str.encode)

    for message in consumer:
        data = message.value.decode('utf-8')
        try:
            ingest_params = json.loads(data)
        except Exception as e:
            print("Exception: ", e)
            continue

        if 'monitoringData' in ingest_params:
            monitoring_data = ingest_params['monitoringData']
        elif 'MonitoringData' in ingest_params:
            monitoring_data = ingest_params['MonitoringData']
        else:
            # expected field is missing; nothing we can do
            print("monitoringData field is missing")
            continue

        if 'transactionID' in monitoring_data:
            transaction_id = monitoring_data['transactionID']
        elif 'TransactionID' in monitoring_data:
            transaction_id = monitoring_data['TransactionID']
        elif 'transactionID' in ingest_params:
            transaction_id = ingest_params['TransactionID']
        elif 'TransactionID' in ingest_params:
            transaction_id = ingest_params['TransactionID']
        else:
            # expected field is missing; nothing we can do
            print("transactionID field is missing")
            continue

        if transaction_id not in mapping_table:
            continue

        kafka_topic_out = mapping_table[transaction_id]
        producer.send(kafka_topic_out, value=data)
        producer.flush()



def init_stream_data():
    global kafka_url
    kafka_url = os.getenv('KAFKA_URL', '127.0.0.1:9092')
    global kafka_topic_in
    kafka_topic_in = os.getenv('KAFKA_TOPIC_IN', 'dl_stream_topic')
    t = threading.Thread(target=handle_stream_data)
    t.start()
    return

def register_transaction_topic(transactionId, body):  # noqa: E501
    """register transactionId for which data should be streamed

     # noqa: E501

    :param transactionId: 
    :type transactionId: str
    :param body: Parameters to get entries related to transactionId
    :type body: dict | bytes

    :rtype: None
    """
    print("register_transaction_topic, transactionId = ", transactionId)
    if connexion.request.is_json:
        body = TransactionQuery.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        raise("content is not json")
    target_topic = body.transaction_info.topic
    mapping_table[transactionId] = target_topic
    print("mapping_table = ", mapping_table)
    return


def unregister_transaction_topic(transactionId, body):  # noqa: E501
    """stop stream data for specified  transactionId

     # noqa: E501

    :param transactionId: 
    :type transactionId: str
    :param body: Parameters to unregister streaming for transactionId
    :type body: dict | bytes

    :rtype: None
    """
    print("unregister_transaction_topic, transactionId = ", transactionId)
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        raise("content is not json")
    if transactionId in mapping_table:
        del mapping_table[transactionId]
    else:
        msg = 'transactionId %s not registered ' % transactionId
        return Response("{'error message':'" + msg + "'\n", status=404, mimetype='application/json')
    print("mapping_table = ", mapping_table)
    return
