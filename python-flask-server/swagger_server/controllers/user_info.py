
import os
import json

from swagger_server.models.user import User
from swagger_server.models.user_resources import UserResources
from swagger_server.models.pipeline_info import PipelineInfo

Users = dict()

DATALAKE_BASE_DIR = os.path.expanduser('~') + '/.datalake_info'

def recover_state():
    files = os.listdir(DATALAKE_BASE_DIR)
    print("files = ", files)
    for f in files:
        print ("f = ", f)
        dir_name_user = DATALAKE_BASE_DIR + '/' + f


def init_users():
    if not os.path.exists(DATALAKE_BASE_DIR):
        os.mkdir(DATALAKE_BASE_DIR)
        return
    else:
        # recover old state
        recover_state()
        return


def persist_user(user_id, available_resources):
    print("entering persist_user")
    print("user_id = ", user_id)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id
    os.mkdir(dir_name)
    file_name = dir_name + '/' + 'available_resources'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(available_resources, f, ensure_ascii=False, indent=4)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/predefined_pipelines'
    os.mkdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines'
    os.mkdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services'
    os.mkdir(dir_name)
    print("exiting persist_user")

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
    print("entering persist_pipeline")
    print("user_id = ", user_id)
    print("pipeline_info = ", pipeline_info)
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
    print("exiting persist_pipeline")

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
    file_name = dir_name + '/' + 'container_definition'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(container_definition, f, ensure_ascii=False, indent=4)

def unpersist_service(user_id, service_id):
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services/' + service_id
    file_name = dir_name + '/' + 'container_definition'
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
        print("entering UserInfo add_pipeline")
        print("len of predefinedPipes = ", len(self.predefinedPipes))
        if predefined_pipeline:
            self.predefinedPipes.append(pipeline_info)
        else:
            self.pipelineInfoList.append(pipeline_info)
        persist_pipeline(self.user.user_id, pipeline_info, predefined_pipeline)
        print("len of predefinedPipes = ", len(self.predefinedPipes))
        print("exiting UserInfo add_pipeline")

    def del_pipeline(self, p, predefined_pipeline: bool):
        print("entering UserInfo del_pipeline")
        print("len of predefinedPipes = ", len(self.predefinedPipes))
        unpersist_pipeline(self.user.user_id, p.pipeline_metadata.pipeline_id, predefined_pipeline)
        if predefined_pipeline:
            self.predefinedPipes.remove(p)
        else:
            self.pipelineInfoList.remove(p)
        print("len of predefinedPipes = ", len(self.predefinedPipes))
        print("exiting UserInfo del_pipeline")

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
