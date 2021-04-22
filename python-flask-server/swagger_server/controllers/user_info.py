
import os
import json

from swagger_server.models.user import User
from swagger_server.models.user_resources import UserResources
from swagger_server.models.pipeline_info import PipelineInfo

Users = dict()

DATALAKE_BASE_DIR = os.path.expanduser('~') + '/.datalake_info'

def persist_init():
    if not os.path.exists(DATALAKE_BASE_DIR):
        os.mkdir(DATALAKE_BASE_DIR)
        return
    else:
        # TODO: recover old state
        return


def persist_user(user_id, available_resources):
    dir_name = DATALAKE_BASE_DIR + '/' + user_id
    os.mkdir(dir_name)
    file_name = dir_name + '/' + 'available_resources'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(available_resources, f, ensure_ascii=False, indent=4)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines'
    os.mkdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services'
    os.mkdir(dir_name)

def unpersist_user(user_id):
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines'
    os.rmdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/services'
    os.rmdir(dir_name)
    dir_name = DATALAKE_BASE_DIR + '/' + user_id
    file_name = dir_name + '/' + 'available_resources'
    os.remove(file_name)
    os.rmdir(dir_name)

def persist_pipeline(user_id, pipeline_info):
    pipeline_metadata = pipeline_info.pipeline_metadata
    pipeline_definition = pipeline_info.pipeline_definition
    pipeline_id = pipeline_metadata.pipeline_id
    dir_name = DATALAKE_BASE_DIR + '/' + user_id + '/pipelines/' + pipeline_id
    os.mkdir(dir_name)
    file_name = dir_name + '/' + 'input_topic'
    file_p = open(file_name, 'w')
    file_p.write(pipeline_metadata.input_topic)
    file_p.close()
    file_name = dir_name + '/' + 'pipeline_definition'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(pipeline_definition, f, ensure_ascii=False, indent=4)

def unpersist_pipeline(user_id, pipeline_id):
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

    def __init__(self, user: User, userResources: UserResources, predefindPipes):
        self.user = user
        self.userResources = userResources
        self.predefinedPipes = predefindPipes
        self.pipelineInfoList = list()
        self.serviceInfoList = list()

    def add_pipeline(self, pipeline_info):
        self.pipelineInfoList.append(pipeline_info)
        persist_pipeline(self.user.user_id, pipeline_info)

    def del_pipeline(self, p):
        unpersist_pipeline(self.user.user_id, p.pipeline_metadata.pipeline_id)
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
