import os
import kubernetes
import sys
import json

from swagger_server.controllers import kafka_api

k8s_proxy_server = None

DATALAKE_NAMESPACE = 'datalake'

def set_k8s_proxy(p):
    global k8s_proxy_server
    k8s_proxy_server = p

def get_k8s_proxy():
    global k8s_proxy_server
    return k8s_proxy_server

class K8s_Proxy:
    def __init__(self):
        # set up k8s proxy
        # use load_kube_config when running not inside a pod
        kubernetes.config.load_kube_config()
        # use load_incluster_config when running inside a pod
        #kubernetes.config.load_incluster_config()
        self.api = kubernetes.client.CustomObjectsApi()
        self.core_api = kubernetes.client.CoreV1Api()
        self.app_api = kubernetes.client.api.apps_v1_api.AppsV1Api()

        self.k8s_url = os.getenv('KUBERNETES_URL', '127.0.0.1:8443')
        print("k8_url = ", self.k8s_url)

    def load_workflow_template(self, template):
        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="workflows",
            body=template
        )
        return response

    def delete_workflow_template(self, pipeline_id):
        response = self.api.delete_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="workflows",
            name=pipeline_id,
            body=kubernetes.client.V1DeleteOptions()
        )
        return response

    def create_eventsource(self, user_id, qualifier, pipeline_number):
        kafka_proxy_server = kafka_api.get_kafka_proxy()

        event_source_name = '%s-%s-%s' % (user_id, qualifier, str(pipeline_number))
        event_source_template = {
            'apiVersion': 'argoproj.io/v1alpha1',
            'kind': 'EventSource',
            'metadata': {
                'name': event_source_name
            },
            'spec': {
                'kafka': {}
            }
        }

        _spec_kafka_template = {
            'url': kafka_proxy_server.kafka_url,
            'topic': event_source_name,
            'jsonBody': True,
            'partition': "0",
            'connectionBackoff': {
                'duration': 10000000000,
                'steps': 5,
                'factor': 2,
                'jitter': 0.2,
            }
        }

        kafka_key = '%s-kafka' % event_source_name
        #event_source_template['spec']['kafka'][kafka_key] = _spec_kafka_template
        event_source_template['spec']['kafka'][event_source_name] = _spec_kafka_template

        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="eventsources",
            body=event_source_template
        )
        print("create_eventsource, response = ", response)
        return event_source_name, kafka_key

    def delete_eventsource(self, event_source_name):
        response = self.api.delete_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="eventsources",
            name=event_source_name,
            body=kubernetes.client.V1DeleteOptions()
        )
        print("delete_eventsource, response = ", response)

    def create_sensor(self, event_name, kafka_key, workflow):
        sensor_name = '%s-job' % (event_name)
        trigger_name = '%s-trigger' % (event_name)
        sensor_template = {
            'apiVersion': 'argoproj.io/v1alpha1',
            'kind': 'Sensor',
            'metadata': {
                'name': sensor_name
                },
            'spec': {
                'template': {
                    'serviceAccountName': 'argo-events-sa'
                    },
                'dependencies': [ {
                    'name': 'my_dep',
                    'eventSourceName': event_name,
                    'eventName': kafka_key,
                    } ],
                'triggers': [ {
                    'template': { 
                        'name': trigger_name,
                        'k8s': { 
                            'group': 'argoproj.io',
                            'version': 'v1alpha1',
                            'resource': 'workflows',
                            'operation': 'create',
                            'source': { },
                            'parameters': [ {
                                'src': { 
                                    'dependencyName': 'my_dep',
                                    'dataKey': 'body'
                                    },
                                'dest': 'spec.arguments.parameters.0.value',
                                } ]
                            }
                        }
                    } ]
                }
            }
        sensor_template['spec']['triggers'][0]['template']['k8s']['source']['resource'] = workflow
        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="sensors",
            body=sensor_template
        )
        print("create_sensor, response = ", response)
        #TODO save the created sensor id somewhere
        return response

    def delete_sensor(self, pipeline_id):
        response = self.api.delete_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="sensors",
            name=pipeline_id,
            body=kubernetes.client.V1DeleteOptions()
        )
        print("delete_sensor, response = ", response)
        return response

    def create_deployment(self, deployment_def):
        response = self.app_api.create_namespaced_deployment(DATALAKE_NAMESPACE, deployment_def)
        name = response.metadata.name
        return name

    def create_service(self, service_def):
        response = self.core_api.create_namespaced_service(DATALAKE_NAMESPACE, service_def)
        name = response.metadata.name
        return response

    def delete_deployment(self, name):
        response = self.app_api.delete_namespaced_deployment(name, DATALAKE_NAMESPACE)
        return

    def delete_service(self, name):
        response = self.core_api.delete_namespaced_service(name, DATALAKE_NAMESPACE),
        return
