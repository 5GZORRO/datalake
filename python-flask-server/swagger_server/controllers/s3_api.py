import os
import io

from minio import Minio
from minio.error import S3Error


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
        self.s3_url = os.getenv('S3_URL', '127.0.0.1:9000')
        print("s3_url ", self.s3_url)

        s3_access_key = os.getenv('S3_ACCESS_KEY', 'user')
        s3_secret_key = os.getenv('S3_SECRET_KEY', 'password')
        client = Minio(
            self.s3_url,
            access_key=s3_access_key,
            secret_key=s3_secret_key,
            secure=False,
        )
        self.client = client

    def create_bucket(self, user_id, bucket_id):
        #TODO use user_id to set permissions
        print("entering create_bucket")
        long_bucket_name = user_id + '-' + bucket_id
        try:
            found = self.client.bucket_exists(long_bucket_name)
            if not found:
                self.client.make_bucket(long_bucket_name)
            else:
                print("Bucket ", long_bucket_name, " already exists")
            print("exiting create_bucket")
            return long_bucket_name
        except Exception as e:
            print("Exception: ", str(e))
            return None

    def delete_bucket(self, long_bucket_name):
        found = self.client.bucket_exists(long_bucket_name)
        if found:
            self.client.remove_bucket(long_bucket_name)
            ret = 204
        else:
            print("Bucket ", long_bucket_name, "not found ")
            ret = 404
        return ret

