import os

from swagger_server.models.pipeline_metadata import PipelineMetadata
from swagger_server.models.pipeline_info import PipelineInfo
from swagger_server.controllers import k8s_api
from swagger_server.controllers.dl_global_services import dl_stream_data_server_topic

image_pull_secrets = os.getenv('IMAGE_PULL_SECRETS', 'datalakeregistrykey')
image_repository = os.getenv('IMAGE_REPOSITORY', 'docker.pkg.github.com/5gzorro/datalake/')

def create_predefined_pipelines(user_id, s3_available : bool):
    print("entering create_predefined_pipelines")
    predefined_pipes = list()
    pipeline_topics = { }
    if not s3_available:
        return pipeline_topics, predefined_pipes
    # create default ingest metrics pipeline
    # TODO: perhaps move this to a config file yaml and have a more general mechanism to add predefined pipelines
    datalake_images_version = os.getenv('DATALAKE_IMAGES_VERSION', '1.0')
    ingest_def = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Workflow",
        "metadata": {
            "generateName": "ingest-pipeline-"
        },
        "spec": {
            "entrypoint": "ingest-and-index",
            "imagePullSecrets": [
                { "name": image_pull_secrets }
            ],
            "arguments": {
                "parameters": [ {
                    "name": "args",
                    "value": "my args"
                } ]
            },
            "templates": [
              {
                "name": "ingest-and-index",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "steps": [
                    [ {
                        "name": "copy-to-topic1",
                        "template": "copy-to-topic",
                        "arguments": {
                            "parameters": [ {
                                "name": "args",
                                "value": "{{inputs.parameters.args}}"
                            } ]
                        }
                    } ],
                    [ {
                        "name": "ingest1",
                        "template": "ingest",
                        "arguments": {
                            "parameters": [ {
                                "name": "args",
                                "value": "{{inputs.parameters.args}}"
                            } ]
                        }
                    } ],
                    [ {
                        "name": "index1",
                        "template": "metrics-index",
                        "arguments": {
                            "parameters": [ {
                                "name": "args",
                                "value": "{{steps.ingest1.outputs.result}}"
                            } ]
                        }
                    } ]
                ]
              },
              {
                "name": "copy-to-topic",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "container": {
                    "image": image_repository+"/copy_to_topic:"+datalake_images_version,
                    "env": [
                        { "name": "KAFKA_URL",
                        "value": os.getenv('KAFKA_URL', '127.0.0.1:9092') },
                        { "name": "KAFKA_TOPIC",
                        "value": dl_stream_data_server_topic },
                    ],
                    "command": [ "python", "./copy_to_topic.py" ],
                    "args": ["{{inputs.parameters.args}}"],
                    "resources": {
                        "limits": {
                            "memory": "32Mi",
                            "cpu": "100m"
                        }
                    }
                }
              },
              {
                "name": "ingest",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "container": {
                    "image": image_repository+"/ingest:"+datalake_images_version,
                    "env": [
                        { "name": "S3_URL",
                        "value": os.getenv('S3_URL', '127.0.0.1:9000') },
                        { "name": "S3_ACCESS_KEY",
                        "value": os.getenv('S3_ACCESS_KEY', 'user') },
                        { "name": "S3_SECRET_KEY",
                        "value": os.getenv('S3_SECRET_KEY', 'password') },
                    ],
                    "command": [ "python", "./ingest.py" ],
                    "args": ["{{inputs.parameters.args}}"],
                    "resources": {
                        "limits": {
                            "memory": "32Mi",
                            "cpu": "100m"
                        }
                    }
                }
              },
              {
                "name": "metrics-index",
                "inputs": {
                    "parameters": [ {
                        "name": "args"
                    } ]
                },
                "container": {
                    "image": image_repository+"/metrics_index:"+datalake_images_version,
                    "env": [
                        { "name": "POSTGRES_HOST",
                        "value": os.getenv("POSTGRES_HOST", "127.0.0.1") },
                    ],
                    "command": [ "python", "./metrics_index.py" ],
                    "args": ["{{inputs.parameters.args}}"],
                    "resources": {
                        "limits": {
                            "memory": "32Mi",
                            "cpu": "100m"
                        }
                    }
                }
              }
            ]
        }
    }
    k8s_proxy_server = k8s_api.get_k8s_proxy()
    try:
        ingest_topic, kafka_key = k8s_proxy_server.create_eventsource(user_id, 'in', pipeline_number=0)
        print("ingest_topic = ", ingest_topic)
        response = k8s_proxy_server.create_sensor(ingest_topic, kafka_key, ingest_def)
        pipeline_id = response['metadata']['name']
        pipe_metadata = PipelineMetadata(pipeline_id, ingest_topic)
        pipe_info = PipelineInfo(pipe_metadata, ingest_def)
        pipeline_topics["resourceMetricsIngestPipeline"] = ingest_topic
        predefined_pipes.append(pipe_info)
    except Exception as e:
        print("Exception: ", str(e))

    # Add here additional pipelines, as needed

    return pipeline_topics, predefined_pipes

