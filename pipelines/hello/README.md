# Hello World example

This directory contains an Argo workflow template (in json format) for a Hello World service.

Use the datalake `POST` command on `datalake/v1/pipeline`, with `pipelineDefinition` set to the contents of `hello_pipeline.json`, to create the hello world service.
The datalake will return an `inputTopic` parameter which should be used to post data to the service via the specified kafka topic.
When data is sent to the `inputTopic` topic, it triggers the pipeline to run and the data is passed to the running program as an argument (argv[1]). 


