
import os
import kubernetes
import yaml
import sys

k8s_proxy_server = None

def set_k8s_proxy(p):
    print("entering set_k8s_proxy ")
    global k8s_proxy_server
    print("type = ", type(k8s_proxy_server))
    k8s_proxy_server = p
    print("type = ", type(k8s_proxy_server))
    print("exiting set_k8s_proxy ")

def get_k8s_proxy():
    print("entering get_k8s_proxy ")
    global k8s_proxy_server
    print("type = ", type(k8s_proxy_server))
    print("exiting get_k8s_proxy ")
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
        content = file1.read()
        lines = content.splitlines()
        conf_info = {}
        for line in lines:
            # extract the defined fields and their values
            line2 = line.split(':', 1)
            conf_info[line2[0].strip()] = line2[1].strip()
        self.conf_info = conf_info

    def load_workflow_template(self, template):
        print("entering load_workflow_template")
        print("template = ", template)
        response = self.api.create_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argo-events",
            plural="workflows",
            body=template
        )
        print("response = ", response)
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
        print("response = ", response)
        print("exiting delete_template")
        return response

