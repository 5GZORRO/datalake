
import os
import sys
import json
import psycopg2

DATALAKE_DB = "datalake"
DATALAKE_DB_TABLE = "datalake_metrics"
DATALAKE_DB_USER = "datalake_user"
DATALAKE_DB_USER_PW = "datalake_pw"

def metrics_index(args):
    # args is expected to be a str representing a json dictionary with the appropriate keys
    try:
        # verify structure of the data; create an exception if dictionary structure is not correct
        metrics_params = json.loads(args)

        resoure_id = metrics_params['resourceID']
        reference_id = metrics_params['referenceID']
        metric_name = metrics_params['metricName']
        metric_value = metrics_params['metricValue']
        timestamp = metrics_params['timestamp']
        storage_location = metrics_params['storageLocation']
    except Exception as e:
        print("Exception =", e)
        return

    # place the data in database
    db_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
    conn = psycopg2.connect(
        host=db_host,
        database=DATALAKE_DB,
        user=DATALAKE_DB_USER,
        password=DATALAKE_DB_USER_PW)
    cur = conn.cursor()
    sql = "INSERT INTO datalake_metrics (resourceID, referenceID, metricName, metricValue, timestamp, storageLocation) VALUES (%s, %s, %s, %s, %s, %s);"
    cur.execute(sql, (resoure_id, reference_id, metric_name, metric_value, timestamp, storage_location))
    cur.close()
    conn.commit()
    conn.close()

def main():
    # extract paramters from argv[1]
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '{}'
    metrics_index(args)
    print(args)

if __name__ == '__main__':
    main()

