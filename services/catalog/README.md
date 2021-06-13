# Datalake Catalog service

## Overview
This repository contains code and other files to implement the 5GZORRO datalake catalog service.

Data is placed into the catalog database.
The catalog service looks up data in the database and returns to requestor, based on resource_id, reference_id, etc.

# Data formats of different versions

## Version 1.1
The format of the expected ingest data is:
```
data = {
    "monitoringData": {
      "metricName": "http://www.provider.com/metrics/availability",
      "metricValue": "0.453",
      "transactionID": "7777",
      "productID": "8888",
      "instanceID": "2",
      "resourceID": "X",
      "referenceID": "Y",
      "timestamp": "the time which the metric was measured"
    },
    "operatorID": "id_example",
    "businessID": "business_id_flow",
    "networkID": "network_slice_id"
}
```

The schema for the database is:
```
CREATE TABLE datalake_metrics_1_1(
           seq_id SERIAL PRIMARY KEY,
		 resourceID VARCHAR,
		 referenceID VARCHAR,
		 transactionID VARCHAR,
		 productID VARCHAR,
		 instanceID VARCHAR,
		 metricName VARCHAR,
		 metricValue VARCHAR,
		 timestamp VARCHAR,
		 storageLocation VARCHAR
);


grant all privileges on table datalake_metrics_1_1 to datalake_user;
grant all privileges on sequence datalake_metrics_1_1_seq_id_seq to datalake_user;

```



## Version 1.0
The format of the expected ingest data is:
```
    monitoring_data = {
            "resourceID": <resource-id>
            "referenceID": <reference-id>
            "metricName": <metric-name>
            "metricsData": <metric-value-json>
            "timestamp": <timestamp>
            }
    postMonitoringDataDict = {
            "OperatorID": <operator-id>,
            "MonitoringData": monitoring_data,
            "StorageLocation": <target-bucket>,
            "DataHash": <data-hash>
            }

```
The schema of the database is as follows:

```
CREATE TABLE datalake_metrics(
         transaction_id SERIAL PRIMARY KEY,
         resourceID VARCHAR,
         referenceID VARCHAR,
         metricName VARCHAR,
         metricValue VARCHAR,
         timestamp VARCHAR,
         storageLocation VARCHAR
);

grant all privileges on table datalake_metrics to datalake_user;
grant all privileges on sequence datalake_metrics_seq_id_seq to datalake_user;

```
