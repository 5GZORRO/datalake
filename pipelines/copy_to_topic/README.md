# Ingest Service

## Overview
This component copies data from its input argument and places the recieved data in the specified kafka topic. It then copies the original input to the output, so it can be consumed by the next item in the pipeline.

## Requirements
Python 3.6

## Create Docker container

```
docker build -t copy_to_topic .
```

## Push container to repository
```
docker build -t docker.pkg.github.com/5gzorro/datalake/copy_to_topic:latest .
docker push docker.pkg.github.com/5gzorro/datalake/copy_to_topic:latest
```


### Run

Use the copy_to_topic_pipeline.json to load a pipeline that runs the copy_to_topic container whenever data arrives.

