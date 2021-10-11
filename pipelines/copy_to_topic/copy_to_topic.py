#!/usr/bin/env python3

import json
import os
import sys

from kafka import KafkaProducer

def copy_to_topic(data):
    # place the data into the topic provided in environment variable
    try:
        kafka_topic = os.getenv('KAFKA_TOPIC', 'dl_stream_topic')
        kafka_url = os.getenv('KAFKA_URL', '127.0.0.1:9092')
        producer = KafkaProducer(bootstrap_servers=[kafka_url],
                         value_serializer=str.encode)
        producer.send(kafka_topic, value=data)

    except Exception as e:
        print("Exception: ", str(e))

def main():
    # extract paramters from argv[1]
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '{}'
    copy_to_topic(args)
    # output the original input to next item in the pipeline
    print(args)



if __name__ == '__main__':
    main()

