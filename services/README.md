# How datalake services work

Datalake services are based on Kubernetes deployments and services.

A datalake service is essentially a Docker container running as a deployment on Kubernetes.
The service template defines which Docker container image to run.
Input/output of the datalake service should be performed using a Kafka input and a Kafka output topic.
The following environment variables are provided by the datalake API and should be used by the Docker container to use the input and output topics: KAFKA_URL, KAFKA_TOPIC_IN, KAFKA_TOPIC_OUT.
For an example, see the copy_data service (in services/copy_data), which simply copies data from its input topic to its output topic.
The input required to define the service is the part of the Kubernetes job yaml (or json) that usually comes under `containers`.
For the copy_data service, the json required is the following:

```
{
    "name": "copy-data",
    "image": "copy_data"
}
```
Perform a `POST datalake/v1/service` operation with the above data to run the specified container on Kubernetes.

In general, only the Kafka topics should be used for input/output.
Some privileged services need to provide ports (e.g. to provide a REST interface).
In this case, ports may be specified, and these are exposed via a Kubernets service.

For example, to run nginx web server, the following container definition is required.

```
{
    "name": "nginx",
    "image": "nginx:1.14.2",
    "ports": [ {
        "name": "web",
        "containerPort": 80,
        "protocol": "TCP"
  } ]
}
```
The main parameters are the `image` parameter and ports needed to be made available.
