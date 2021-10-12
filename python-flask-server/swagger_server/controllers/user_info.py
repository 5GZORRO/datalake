
import os
import json

from swagger_server.models.user import User
from swagger_server.models.user_resources import UserResources
from swagger_server.models.pipeline_info import PipelineInfo
from swagger_server.models.pipeline_metadata import PipelineMetadata
from swagger_server.models.service_info import ServiceInfo
from swagger_server.models.service_metadata import ServiceMetadata
from swagger_server.controllers import dl_global_services


Users = dict()

next_index = 101

DATALAKE_BASE_DIR = os.path.expanduser('~') + '/.datalake_info'

def recover_service(service_dir_name, service_id):
    print("entering recover_service")
    print("service_dir_name = ", service_dir_name, "service_id = ", service_id)
    dir_name = service_dir_name + '/' + service_id

    file_name = dir_name + '/' + 'container_definition'
    f = open(file_name, 'r', encoding='utf-8')
    container_def = json.load(f)
    f.close()

    #file_name = dir_name + '/' + 'ports'
    #f = open(file_name, 'r', encoding='utf-8')
    #ports = json.load(f)
    #f.close()

    file_name = dir_name + '/' + 'input_topic'
    f = open(file_name, 'r', encoding='utf-8')
    input_topic = f.read()
    f.close()

    file_name = dir_name + '/' + 'output_topic'
    f = open(file_name, 'r', encoding='utf-8')
    output_topic = f.read()
    f.close()

    #service_metadata = ServiceMetadata(service_id, ports)
    service_metadata = ServiceMetadata(service_id, input_topic, output_topic)
    service_info = ServiceInfo(service_metadata, container_def)

    return service_info

def recover_pipeline(pipeline_dir_name, pipeline_id):
    print("entering recover_pipeline")
    print("pipeline_dir_name = ", pipeline_dir_name, "pipeline_id = ", pipeline_id)
    dir_name = pipeline_dir_name + '/' + pipeline_id

    file_name = dir_name + '/' + 'input_topic'
    f = open(file_name, 'r', encoding='utf-8')
    input_topic = f.read()
    f.close()

    file_name = dir_name + '/' + 'pipeline_definition'
    f = open(file_name, 'r', encoding='utf-8')
    pipeline_def = json.load(f)
    f.close()

    pipe_metadata = PipelineMetadata(pipeline_id, input_topic)
    pipe_info = PipelineInfo(pipe_metadata, pipeline_def)
    return pipe_info

def recover_user_state(user_id):
    print("entering recover_user_state")
    dir_name = DATALAKE_BASE_DIR + '/' + user_id

    file_name = dir_name + '/' + 'available_resources'
    f = open(file_name, 'r', encoding='utf-8')
    available_resources = json.load(f)
    user_resources = UserResources(user_id, available_resources)
    f.close()

    # Fix the address of the catalog server, in case it changed
    available_resources['urls']['dl_catalog_server_url'] = dl_global_services.dl_catalaog_server_url
    available_resources['urls']['dl_stream_data_server_url'] = dl_global_services.dl_stream_data_server_url

    user = User(user_id, 'blah')

    u_info = UserInfo(user, user_resources)

    predefinedPipes = list()
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/predefined_pipelines'
    files = os.listdir(dir_name)
    for pipeline_id in files:
        pipe_info = recover_pipeline(dir_name, pipeline_id)
        predefinedPipes.append(pipe_info)
    u_info.predefinedPipes = predefinedPipes

    global next_index
    max_index = next_index
    pipelines = list()
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines'
    files = os.listdir(dir_name)
    for pipeline_id in files:
        pipe_info = recover_pipeline(dir_name, pipeline_id)
        pipelines.append(pipe_info)
        p_index = int(pipeline_id[-7:-4])
        if p_index > max_index:
            max_index = p_index
    u_info.pipelineInfoList = pipelines

    services = list()
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services'
    files = os.listdir(dir_name)
    for service_id in files:
        s_info = recover_service(dir_name, service_id)
        services.append(s_info)
        p_index = int(service_id[-3:])
        if p_index > max_index:
            max_index = p_index
    u_info.serviceInfoList = services
    Users[user_id] = u_info
    next_index = max_index + 1

def recover_state():
    print("entering recover_state")
    files = os.listdir(DATALAKE_BASE_DIR)
    print("files = ", files)
    for user_id in files:
        recover_user_state(user_id)


def init_users():
    if not os.path.exists(DATALAKE_BASE_DIR):
        os.mkdir(DATALAKE_BASE_DIR)
        return
    else:
        # recover old state
        recover_state()
        return


def persist_user(user_id, available_resources):
    dir_name = DATALAKE_BASE_DIR + '/' + user_id
    os.mkdir(dir_name)

    file_name = dir_name + '/' + 'available_resources'
    # TODO: close all unneeded files
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(available_resources, f, ensure_ascii=False, indent=4)

    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/predefined_pipelines'
    os.mkdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines'
    os.mkdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services'
    os.mkdir(dir_name)

def unpersist_user(user_id):
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/predefined_pipelines'
    os.rmdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines'
    os.rmdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services'
    os.rmdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id
    file_name = dir_name + '/' + 'available_resources'
    os.remove(file_name)
    os.rmdir(dir_name)

def persist_pipeline(user_id, pipeline_info, predefined_pipeline: bool):
    pipeline_metadata = pipeline_info.pipeline_metadata
    pipeline_definition = pipeline_info.pipeline_definition
    pipeline_id = pipeline_metadata.pipeline_id
    if predefined_pipeline:
        dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/predefined_pipelines/' + pipeline_id
    else:
        dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines/' + pipeline_id
    os.mkdir(dir_name)
    file_name = dir_name + '/' + 'input_topic'
    file_p = open(file_name, 'w')
    file_p.write(pipeline_metadata.input_topic)
    file_p.close()
    file_name = dir_name + '/' + 'pipeline_definition'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(pipeline_definition, f, ensure_ascii=False, indent=4)

def unpersist_pipeline(user_id, pipeline_id, predefined_pipeline: bool):
    if predefined_pipeline:
        dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/predefined_pipelines/' + pipeline_id
    else:
        dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines/' + pipeline_id
    file_name = dir_name + '/' + 'input_topic'
    os.remove(file_name)
    file_name = dir_name + '/' + 'pipeline_definition'
    os.remove(file_name)
    os.rmdir(dir_name)

def persist_service(user_id, service_info):
    service_metadata = service_info.service_metadata
    container_definition = service_info.container_definition
    service_id = service_metadata.service_id
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services/' + service_id
    os.mkdir(dir_name)

    file_name = dir_name + '/' + 'input_topic'
    file_p = open(file_name, 'w')
    file_p.write(service_metadata.input_topic)
    file_p.close()

    file_name = dir_name + '/' + 'output_topic'
    file_p = open(file_name, 'w')
    file_p.write(service_metadata.output_topic)
    file_p.close()

    #file_name = dir_name + '/' + 'ports'
    #with open(file_name, 'w', encoding='utf-8') as f:
        #json.dump(service_metadata.ports, f, ensure_ascii=False, indent=4)

    file_name = dir_name + '/' + 'container_definition'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(container_definition, f, ensure_ascii=False, indent=4)

def unpersist_service(user_id, service_id):
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services/' + service_id
    file_name = dir_name + '/' + 'container_definition'
    os.remove(file_name)
    #file_name = dir_name + '/' + 'ports'
    #os.remove(file_name)
    file_name = dir_name + '/' + 'input_topic'
    os.remove(file_name)
    file_name = dir_name + '/' + 'output_topic'
    os.remove(file_name)
    os.rmdir(dir_name)


class UserInfo():

    def __init__(self, user: User, userResources: UserResources):
        self.user = user
        self.userResources = userResources
        self.predefinedPipes = list()
        self.pipelineInfoList = list()
        self.serviceInfoList = list()

    def add_pipeline(self, pipeline_info, predefined_pipeline: bool):
        if predefined_pipeline:
            self.predefinedPipes.append(pipeline_info)
        else:
            self.pipelineInfoList.append(pipeline_info)
        persist_pipeline(self.user.user_id, pipeline_info, predefined_pipeline)

    def del_pipeline(self, p, predefined_pipeline: bool):
        unpersist_pipeline(self.user.user_id, p.pipeline_metadata.pipeline_id, predefined_pipeline)
        if predefined_pipeline:
            self.predefinedPipes.remove(p)
        else:
            self.pipelineInfoList.remove(p)

    def add_service(self, service_info):
        self.serviceInfoList.append(service_info)
        persist_service(self.user.user_id, service_info)

    def del_service(self, s):
        self.serviceInfoList.remove(s)
        unpersist_service(self.user.user_id, s.service_metadata.service_id)

def get_users():
    return list(Users)

def get_user(user_id):
    return Users[user_id]

def add_user(user_id, user_info):
    Users[user_id] = user_info
    persist_user(user_id, user_info.userResources.available_resources)

def del_user(user_id):
    unpersist_user(user_id)
    del Users[user_id]
