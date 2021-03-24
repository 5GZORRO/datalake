import os
import kubernetes
import sys

from swagger_server.controllers import kafka_api

k8s_proxy_server = None

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

        self.k8s_url = os.getenv('KUBERNETES_URL', '127.0.0.1:8443')
        print("k8_url = ", self.k8s_url)

    def load_workflow_template(self, template):
        print("entering load_workflow_template")
        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="workflows",
            body=template
        )
        print("exiting load_workflow_template")
        return response

    def delete_workflow_template(self, pipeline_id):
        print("entering delete_workflow_template")
        response = self.api.delete_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="workflows",
            name=pipeline_id,
            body=kubernetes.client.V1DeleteOptions()
        )
        print("exiting delete_workflow_template")
        return response

    def create_eventsource(self, user_id, in_out, pipeline_number):
        print("entering create_eventsource")

        kafka_proxy_server = kafka_api.get_kafka_proxy()

        event_source_name = '%s-%s-%s' % (user_id, in_out, str(pipeline_number))
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

        kafka_key = '%s-event' % event_source_name
        event_source_template['spec']['kafka'][kafka_key] = _spec_kafka_template
        print("event_source_template = ", event_source_template)

        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="eventsources",
            body=event_source_template
        )
        print("response = ", response)
        print("exiting create_eventsource")
        return event_source_name, kafka_key

    def delete_eventsource(self, event_source_name):
        print("Deleting eventsource...")
        print("event_source_name = ", event_source_name)
        self.api.delete_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="eventsources",
            name=event_source_name,
            body=kubernetes.client.V1DeleteOptions()
        )
        print("exiting delete_eventsource...")

    def create_sensor(self, event_name, kafka_key, workflow):
        print("entering create_sensor")
        print("event_name = ", event_name)

        sensor_name = '%s-sensor' % (event_name)
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
        #TODO save the created sensor id somewhere
        print("exiting create_sensor")
        return response

    def delete_sensor(self, pipeline_id):
        print("entering delete_sensor")
        response = self.api.delete_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="sensors",
            name=pipeline_id,
            body=kubernetes.client.V1DeleteOptions()
        )
        print("exiting delete_sensor")
