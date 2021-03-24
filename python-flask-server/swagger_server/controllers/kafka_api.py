import os


from kafka.admin import KafkaAdminClient, NewTopic


kafka_proxy_server = None

def set_kafka_proxy(p):
    global kafka_proxy_server
    kafka_proxy_server = p

def get_kafka_proxy():
    global kafka_proxy_server
    return kafka_proxy_server

class Kafka_Proxy:
    def __init__(self):
        # obtain configuration information - URLs, secrets, etc
        self.kafka_url = os.getenv('KAFKA_URL', '127.0.0.1:9092')
        print("kafka_url = ", self.kafka_url)
        client = KafkaAdminClient(
            bootstrap_servers=self.kafka_url,
            #TODO need to define a DL (datalake) user in kafka
            client_id='DL',
        )
        self.client = client

    def create_topic(self, user_id, topic):
        print("kafka create_topic, topic = ", topic)
        #TODO user user_id to set permissions
        #TODO check if topic already exists
        topic_list = []
        topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        response = self.client.create_topics(new_topics=topic_list, validate_only=False)
        #TODO use user_id to set permissions
        return topic

    def delete_topic(self, topic):
        print("kafka delete_topic, topic = ", topic)
        topic_list = [topic]
        response = self.client.delete_topics(topic_list)
        #TODO check for errors
        return 204
