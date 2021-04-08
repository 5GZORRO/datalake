
from swagger_server.models.user import User
from swagger_server.models.user_resources import UserResources
from swagger_server.models.pipeline_info import PipelineInfo

Users = dict()

class UserInfo():

    def __init__(self, user: User, userResources: UserResources, predefindPipes):
        self.user = user
        self.userResources = userResources
        self.predefinedPipes = predefindPipes
        self.pipelineInfoList = list()


def print_users():
    for u in Users:
        user_info = Users[u]
        print("user = ", str(user_info.user), "resources = ", user_info.userResources, "pipelineInfoList = ", user_info.pipelineInfoList)
