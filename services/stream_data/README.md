# Stream Data Service

## Overview
This service provides data streaming of metrics data to clients.
It is implemented as a swagger-generated OpenAPI REST API in python and is deployed as a Docker container.
It is installed by the Datalake Server as part of the basic services provided to a user of the Datalake.

The API is [here](https://github.com/5GZORRO/datalake/blob/master/services/stream_data/stream_data.html).

A user may register with this service to receive streamed data based on a specified productID.
Whenever monitoring data with the specified productID is detected,
that monitoring data is streamed directly to a (Kafka) topic provided by the registered module.
In this way the registered module receives exactly those monitoring data items that are of interest in a timely manner. 

Instructions to build and package this service are [here](https://github.com/5GZORRO/datalake/tree/master/services/stream_data/python-flask-server).

