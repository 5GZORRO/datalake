# How datalake pipelines work

Datalake pipelines are based on [Argo workflows]( https://github.com/argoproj/argo-workflows/blob/master/examples/README.md).

A pipeline is essentially a function-as-a-service.
The pipeline template defines a sequence of steps to be performed when some event occurs.

The datalake `POST datalake/v1/pipeline` operation defines a Kafka topic to which the user may post data.
Whenever data is received on the pipeline's topic, the pipeline is triggered and the data is passed to the pipeline as a command line argument (argv[1]) of the first step in the pipeline.
Each step of the pipeline may output data, which is then provided as input to the next step in the pipeline.

When calling `POST datalake/v1/pipeline`, set `pipelineDefinition` to the json representation of the argo template for the pipeline.

# Programs that are not function-as-a-service

To run a program that is not function-as-a-service (e.g. a web server with a REST API), we provide the datalake `service`, which is essentially a Kubernetes deployment and service of a single container.
See instructions under the services directory.
