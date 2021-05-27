# Ingest Service

## Overview
This component places data passed as argv[1] into the metrics metadata catalog.

## Requirements
Python 3.6

## Create Docker container

```
docker build -t metrics_index .
```

## Push container to repository
```
docker build -t docker.pkg.github.com/5gzorro/datalake/metrics_index:latest .
docker push docker.pkg.github.com/5gzorro/datalake/metrics_index:latest
```

### Run

This component is part of larger pipeline, preceded by ingest.

