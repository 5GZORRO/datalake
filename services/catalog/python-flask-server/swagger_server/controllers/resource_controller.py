import os
import connexion
import six
import psycopg2

from swagger_server.models.resource_entries_info import ResourceEntriesInfo  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.resource_query import ResourceQuery  # noqa: E501
from swagger_server import util

DATALAKE_DB = "datalake"
DATALAKE_DB_TABLE = "datalake_metrics"
DATALAKE_DB_USER = "datalake_user"
DATALAKE_DB_USER_PW = "datalake_pw"

# postgress python database variables
db_host = None
conn = None
cur = None

def init_catalog_access():
    global db_host
    db_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
    global conn
    conn = psycopg2.connect(
        host=db_host,
        database=DATALAKE_DB,
        user=DATALAKE_DB_USER,
        password=DATALAKE_DB_USER_PW)
    global cur
    cur = conn.cursor()

def process_query(query_specific, time_interval):
    if time_interval:
        start_time = "'%s'" % time_interval.start_time
        end_time = "'%s'" % time_interval.end_time
        sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + query_specific + " AND " + DATALAKE_DB_TABLE + ".timestamp >= " + start_time + " AND " + DATALAKE_DB_TABLE + ".timestamp <= " + end_time
    else:
        sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + query_specific
    cur.execute(sql)
    rows = cur.fetchone()
    content = rows[0]
    if not isinstance(content, list):
        return
    # remove undesired fields from returned content
    for ee in content:
        del ee['seq_id']
    return content


def process_json_parameters():
    if connexion.request.is_json:
        body = ResourceQuery.from_dict(connexion.request.get_json())
    else:
        raise("content is not json")

    # TODO: check user and permissions
    user = body.user_info
    time_interval = body.time_info
    # TODO check for valid user info
    return user, time_interval

def get_reference(referenceId):  # noqa: E501
    """Return entries related to specified reference

     # noqa: E501

    :param referenceId: 
    :type referenceId: str
    :param body: Parameters to get a entries related to resource
    :type body: dict | bytes

    :rtype: List[ResourceEntriesInfo]
    """
    user, time_interval = process_json_parameters()
    query_specific = ".referenceID = '%s'" % referenceId
    content = process_query(query_specific, time_interval)
    return content


def get_resource(resourceId):  # noqa: E501
    """Return entries related to specified resource

     # noqa: E501

    :param resourceId: 
    :type resourceId: str
    :param body: Parameters to get a entries related to resource
    :type body: dict | bytes

    :rtype: List[ResourceEntriesInfo]
    """
    user, time_interval = process_json_parameters()
    query_specific = ".resourceID = '%s'" % resourceId
    content = process_query(query_specific, time_interval)
    return content

def get_product(productId):  # noqa: E501
    """Return entries related to specified product

     # noqa: E501

    :param productId: 
    :type productId: str
    :param body: Parameters to get a entries related to product
    :type body: dict | bytes

    :rtype: List[ResourceEntriesInfo]
    """
    user, time_interval = process_json_parameters()
    query_specific = ".productID = '%s'" % productId
    content = process_query(query_specific, time_interval)
    return content

def get_transaction(transactionId):  # noqa: E501
    """Return entries related to specified transaction

     # noqa: E501

    :param transactionId: 
    :type transactionId: str
    :param body: Parameters to get a entries related to transaction
    :type body: dict | bytes

    :rtype: List[ResourceEntriesInfo]
    """
    user, time_interval = process_json_parameters()
    query_specific = ".transactionID = '%s'" % transactionId
    content = process_query(query_specific, time_interval)
    return content

def get_instance(instanceId):  # noqa: E501
    """Return entries related to specified instance

     # noqa: E501

    :param instanceId: 
    :type instanceId: str
    :param body: Parameters to get a entries related to instance
    :type body: dict | bytes

    :rtype: List[ResourceEntriesInfo]
    """
    user, time_interval = process_json_parameters()
    query_specific = ".instanceID = '%s'" % instanceId
    content = process_query(query_specific, time_interval)
    return content
