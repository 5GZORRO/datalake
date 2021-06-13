import os
import connexion
import six
import psycopg2

from swagger_server.models.resource_entries_info import ResourceEntriesInfo  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

DATALAKE_DB = "datalake"
DATALAKE_DB_TABLE = "datalake_metrics_1_1"
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
    print("get_resouce: referenceId = ", referenceId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".referenceID = '%s'" % referenceId
    cur.execute(sql)
    rows = cur.fetchone()
    content = rows[0]
    return content


def get_resouce(resourceId):  # noqa: E501
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
    print("get_resouce: resourceId = ", resourceId)
    sql = "SELECT json_agg(" + DATALAKE_DB_TABLE + ") FROM " + DATALAKE_DB_TABLE + " WHERE "+ DATALAKE_DB_TABLE + ".referenceID = '%s'" % resourceId
    cur.execute(sql)
    rows = cur.fetchone()
    content = rows[0]
    return content
