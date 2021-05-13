#!/usr/bin/env python3

import os
import sys
from kafka import KafkaConsumer, KafkaProducer
from json import dumps

def main():
    kafka_url = os.getenv('KAFKA_URL', '127.0.0.1:9092')
    kafka_topic_in = os.getenv('KAFKA_TOPIC_IN')
    kafka_topic_out = os.getenv('KAFKA_TOPIC_OUT')
    consumer = KafkaConsumer(
            kafka_topic_in,
            bootstrap_servers=[kafka_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group')

    producer = KafkaProducer(
            bootstrap_servers=[kafka_url],
            value_serializer=lambda x:
            dumps(x).encode('utf-8'))

    for message in consumer:
        content = message.value.decode('utf-8')
        producer.send(kafka_topic_out, value=content)


if __name__ == '__main__':
    main()

