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

        s3_access_key = os.getenv('S3_ACCESS_KEY', 'user')
        s3_secret_key = os.getenv('S3_SECRET_KEY', 'password')
        client = Minio(
            self.s3_url,
            access_key=s3_access_key,
            secret_key=s3_secret_key,
            secure=False,
        )
        self.client = client

    # data is expected to be a string
    def put_object(self, user_id, bucket_name, data, data_hash, timestamp, object_name_prefix):
        found = self.client.bucket_exists(bucket_name)
        # convert data string into a bytes stream to be consumable by s3 client put_object.
        b = data.encode('utf-8')
        value_as_a_stream = io.BytesIO(b)
        if found:
            object_name = object_name_prefix + '/' + timestamp
            # TODO add hash as metadata to object
            rc = self.client.put_object(bucket_name, object_name, value_as_a_stream, len(data))
            ret = 204
        else:
            ret = 404
        return ret
