import os
import connexion
import json
import six
import threading

from flask import Response
from kafka import KafkaConsumer, KafkaProducer

from swagger_server.models.product_query import ProductQuery  # noqa: E501
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

        if 'productID' in monitoring_data:
            product_id = monitoring_data['productID']
        elif 'ProductID' in monitoring_data:
            product_id = monitoring_data['ProductID']
        elif 'productID' in ingest_params:
            product_id = ingest_params['ProductID']
        elif 'ProductID' in ingest_params:
            product_id = ingest_params['ProductID']
        else:
            # expected field is missing; nothing we can do
            print("productID field is missing")
            continue

        if product_id not in mapping_table:
            continue

        kafka_topic_out = mapping_table[product_id]
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

def register_product_topic(productId, body):  # noqa: E501
    """register productId for which data should be streamed

     # noqa: E501

    :param productId: 
    :type productId: str
    :param body: Parameters to get entries related to productId
    :type body: dict | bytes

    :rtype: None
    """
    print("register_product_topic, productId = ", productId)
    if connexion.request.is_json:
        body = ProductQuery.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        raise("content is not json")
    target_topic = body.product_info.topic
    mapping_table[productId] = target_topic
    print("mapping_table = ", mapping_table)
    return


def unregister_product_topic(productId, body):  # noqa: E501
    """stop stream data for specified  productId

     # noqa: E501

    :param productId: 
    :type productId: str
    :param body: Parameters to unregister streaming for productId
    :type body: dict | bytes

    :rtype: None
    """
    print("unregister_product_topic, productId = ", productId)
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        raise("content is not json")
    if productId in mapping_table:
        del mapping_table[productId]
    else:
        msg = 'productId %s not registered ' % productId
        return Response("{'error message':'" + msg + "'\n", status=404, mimetype='application/json')
    print("mapping_table = ", mapping_table)
    return
