# Ingest Service

## Overview
This component ingests data sent to its input topic and places the recieved data as an object in the user's object store under the specified bucket.

## Requirements
Python 3.6

## Create Docker container

```
docker build -t ingest .
```

## Push container to repository
```
docker build -t docker.pkg.github.com/5gzorro/datalake/ingest:latest .
docker push docker.pkg.github.com/5gzorro/datalake/ingest:latest
```


### Run

Use the ingest_pipeline.json to load a pipeline that runs the ingest container whenever data arrives on the input topic.

