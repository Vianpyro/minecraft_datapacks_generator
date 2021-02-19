from .file import File
from .raycast import Raycast

class Workspace():
    def __init__(self, name: str) -> None:
        if name.endswith('.mcfunction'): name.replace('.mcfunction', '', 1)
        self.name = name
        self.files = None
        self.raycasts = None
    def add_file(self, file: File):
        if self.files == None: self.files = []
        self.files.append(file)
    def add_raycast(self, raycast: Raycast):
        if self.raycasts == None: self.raycasts = []
        self.raycasts.append(raycast)