import os

from minio import Minio
from minio.error import S3Error
from swagger_server.controllers.k8s_api import get_k8s_proxy


s3_proxy_server = None

def set_s3_proxy(p):
    global s3_proxy_server
    s3_proxy_server = p

def get_s3_proxy():
    global s3_proxy_server
    return s3_proxy_server

class S3_Proxy:
    def __init__(self):
        # obtain configuration information - URLs, secrets, etc
        self.s3_url = self.kafka_url = os.getenv('S3_URL', '192.168.122.176:9000')

        s3_access_key = os.getenv('S3_ACCESS_KEY', 'user')
        s3_secret_key = os.getenv('S3_SECRETE_KEY', 'password')
        client = Minio(
            self.s3_url,
            access_key=s3_access_key,
            secret_key=s3_secret_key,
            secure=False,
        )
        self.client = client

    def create_bucket(self, user_id, bucket_id):
        #TODO use user_id to set permissions
        long_bucket_name = user_id + '-' + bucket_id
        found = self.client.bucket_exists(long_bucket_name)
        if not found:
            self.client.make_bucket(long_bucket_name)
        else:
            print("Bucket ", long_bucket_name, " already exists")
        s3_bucket_url = self.s3_url + '/' + long_bucket_name
        return long_bucket_name, s3_bucket_url

    def delete_bucket(self, long_bucket_name):
        found = self.client.bucket_exists(long_bucket_name)
        if found:
            self.client.remove_bucket(long_bucket_name)
            ret = 204
        else:
            print("Bucket ", long_bucket_name, "not found ")
            ret = 404
        return ret
