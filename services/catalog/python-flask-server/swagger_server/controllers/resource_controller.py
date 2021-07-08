import os
import connexion
import six
import psycopg2

from swagger_server.models.resource_entries_info import ResourceEntriesInfo  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
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

def process_query(sql):
    cur.execute(sql)
    rows = cur.fetchone()
    content = rows[0]
    ttype = type(content)
    // remove undesired fields from returned content
    for ee in content:
        del ee['seq_id']
    return content


def get_reference(referenceId):  # noqa: E501
    """Return entries related to specified reference

     # noqa: E501

    :param referenceId: 
    :type referenceId: str
    :param body: Parameters to get a entries related to resource
    :type body: dict | bytes

    :rtype: List[ResourceEntriesInfo]
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    # TODO: check user and permissions
    print("get_reference: referenceId = ", referenceId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".referenceID = '%s'" % referenceId
    content = process_query(sql)
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
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    print("get_resource: resourceId = ", resourceId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".resourceID = '%s'" % resourceId
    content = process_query(sql)
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
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    print("get_product: productId = ", productId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".productID = '%s'" % productId
    content = process_query(sql)
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
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    print("get_transaction: transactionId = ", transactionId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".transactionID = '%s'" % transactionId
    content = process_query(sql)
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
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    print("get_instance: instanceId = ", instanceId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".instanceID = '%s'" % instanceId
    content = process_query(sql)
    return content
