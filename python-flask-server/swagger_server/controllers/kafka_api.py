
from kafka.admin import KafkaAdminClient, NewTopic
from swagger_server.controllers.k8s_api import get_k8s_proxy


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
        k8s_proxy_server = get_k8s_proxy()
        # TODO check for all kinds of errors
        self.kafka_url = k8s_proxy_server.urls['kafka_url']
        client = KafkaAdminClient(
            bootstrap_servers=self.kafka_url,
            #TODO need to define a DL (datalake) user in kafka
            client_id='DL',
        )
        self.client = client

    def create_topic(self, user_id, topic):
        #TODO user user_id to set permissions
        topic_list = []
        topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        response = self.client.create_topics(new_topics=topic_list, validate_only=False)
        #TODO use user_id to set permissions
        return topic

    def delete_topic(self, topic):
        topic_list = [topic]
        response = self.client.delete_topics(topic_list)
        #TODO check for errors
        return 204
