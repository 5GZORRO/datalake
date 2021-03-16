
import os
import kubernetes
import yaml
import sys

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

        # obtain configuration information - URLs, etc
        if len(sys.argv) != 2:
            raise Exception('incorrect number of command-line parameters; need parameter conf file')
        conf_file = sys.argv[1]
        file1 = open(conf_file, 'r')
        content = yaml.load(file1)
        if 'urls' in content:
            urls = content['urls']
        else:
            urls = {}
        self.urls = urls
        self.conf = content

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
        """
        Create a kafka sink object for the given tenant. The proper tenant's topic
        is created as well.

        :param user_id: the uuid of the tenant this sink is created for
        :type user_id: ``str`` (supplied in kwargs)

        :param in_out: Defines whether it is an input or output sink
        :type in_out: ``str``

        :param pipeline_number: Index of the pipeline
        :type pipeline_number: ``int``

        :return event_source_name: A unique name of event_source in the format of:
                                   <user_id>-<in_out>-<pipeline_number>
        """

        print("entering create_eventsource")

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
            'url': self.urls['kafka_url'],
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

        event_source_template['spec']['kafka'][event_source_name] = _spec_kafka_template

        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="eventsources",
            body=event_source_template
        )
        print("exiting create_eventsource")
        return event_source_name

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

    def create_sensor(self, sensor_yaml, user_id, event_source_name):
        """
        Create a kafka sensor object for the given tenant. The sensor is bound
        to the eventsource (sink) and get triggered whenever a message is
        posted in its kafka topic.

        :param sensor_yaml: template of the sensor being overridden by
                            user_id and other parameters
        :type sensor_yaml: ``json``

        :param user_id: the uuid of the user this sink is created for
        :type user_id: ``str`` (supplied in kwargs)

        :param event_source_name: The unique event source to link this sensor.
        :type event_source_name: ``str``
        """
        #FIXME: move this to config
        CATALOG_IP = '1.2.3.4'
        CATALOG_PORT = '80'
        OBJECTSTORE_IP = '1.2.3.4'
        OBJECTSTORE_PORT = '80'

        sensor_yaml['metadata']['name'] = '%s' % user_id
        sensor_yaml['spec']['dependencies'][0]['eventSourceName'] = \
            event_source_name
        sensor_yaml['spec']['dependencies'][0]['eventName'] = \
            event_source_name

        _template_k8s_source = sensor_yaml['spec']['triggers'][0]['template']['k8s']['source']
        _template_k8s_source['resource']['metadata']['generateName'] = '%s-pipeline-' % user_id
        _template_k8s_source['resource']['metadata']['labels']['user_id'] = user_id
        parameters = _template_k8s_source['resource']['spec']['arguments']['parameters']

        kafka_ip_prop = find(parameters, lambda p: p['name'] == 'kafka_ip')
        kafka_port_prop = find(parameters, lambda p: p['name'] == 'kafka_port')

        catalog_ip_prop = find(parameters, lambda p: p['name'] == 'catalog_ip')
        catalog_port_prop = find(parameters, lambda p: p['name'] == 'catalog_port')

        catalog_ip_prop['value'] = CATALOG_IP
        catalog_port_prop['value'] = CATALOG_PORT

        objectstore_ip_prop = find(parameters, lambda p: p['name'] == 'objectstore_ip')
        objectstore_port_prop = find(parameters, lambda p: p['name'] == 'objectstore_port')

        objectstore_ip_prop['value'] = OBJECTSTORE_IP
        objectstore_port_prop['value'] = OBJECTSTORE_PORT

        self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="sensors",
            body=sensor_yaml
        )
        sys.stdout.write('Done creating sensor\n')
        return {}

    def create_sensor2(self, event_name, kafka_key, workflow):
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
