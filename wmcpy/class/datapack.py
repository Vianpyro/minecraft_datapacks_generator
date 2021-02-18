from os import mkdir
from shutil import rmtree
from .workspace import Workspace

class Datapack():
    def __init__(self, name, description, version):
        self.name = name
        self.description = description
        self.version = version
        self.workspaces = []
    def add_workspace(self, workspace: Workspace):
        self.workspaces.append(workspace)
    def build(self, path: str, force=False):
        try:
            mkdir(path + '/' + self.name)
        except FileExistsError:
            if force:
                rmtree(path + '/' + self.name)
                mkdir(path + '/' + self.name)
            else:
                raise FileExistsError('dir early exist with this path, add force=True to the function to ignore this error and to delete the dir to re-create it')
        open(path + '/' + self.name + '/pack.mcmeta', 'w+', encoding='utf-8').write(str({ "pack": { "pack_format": int(self.version), "description": self.description}}).replace('\'', '\"'))
        mkdir(path + '/' + self.name + '/data')
        for workspace in self.workspaces:
            mkdir(path + '/' + self.name + '/data/' + workspace.name)
            if workspace.files != None:
                for file in workspace.files:
                    if file != None:
                        mkdir(path + '/' + self.name + '/data/' + workspace.name + '/functions')
                        commands = ''
                        for command in file.commands:
                            commands += command + '\n'
                        open(path + '/' + self.name + '/data/' + workspace.name + '/functions/' + file.name + '.mcfunction', 'w+', encoding='utf-8').write(commands)