##################################
#                                #
#     code by theskyblockman     #
#                                #
##################################
from os import mkdir
from shutil import rmtree

class Workspace():
    def __init__(self, name: str) -> None:
        self.name = name
        self.files = []
class Datapack():
    def __init__(self, name, description, version):
        self.name = name
        self.description = description
        self.version = version
        self.workspaces = []
    def add_workspace(self, workspace: Workspace):
        self.workspaces.append(workspace)
    def build(self, path: str, functions: list, force=False):
        try:
            mkdir(path + '/' + self.name)
        except FileExistsError:
            if force:
                rmtree(path + '/' + self.name)
                mkdir(path + '/' + self.name)
            else:
                raise FileExistsError('dir early exist with this path, add force=True to the function to ignore this error and to delete the dir to re-create it')
        open(path + '/' + self.name + '/pack.mcmeta', 'w+').write(str({ "pack": { "pack_format": self.version, "description": self.description}}).replace('\'', '\"'))
        for workspace in self.workspaces:
            mkdir(path + '/' + self.name + '/' + workspace.name)