class Pack:
    def __init__(self, minecraft_version='1.6.1', description=None, author=None):
        default_pack_format = 7
        minecraft_version_to_pack_format = {
            '1.6.1': 1, '1.6.2': 1, '1.6.4': 1,
            '1.7.2': 1, '1.7.4': 1, '1.7.5': 1, '1.7.6': 1, '1.7.7': 1, '1.7.8': 1, '1.7.9': 1, '1.7.10': 1,
            '1.8': 1, '1.8.1': 1, '1.8.2': 1, '1.8.3': 1, '1.8.4': 1, '1.8.5': 1, '1.8.6': 1, '1.8.7': 1, '1.8.8': 1, '1.8.9': 1,
            '1.9': 2, '1.9.1': 2, '1.9.2': 2, '1.9.3': 2, '1.9.4': 2,
            '1.10': 2, '1.10.1': 2, '1.10.2': 2,
            '1.11': 3, '1.11.1': 3, '1.11.2': 3,
            '1.12': 3, '1.12.1': 3, '1.12.2': 3,
            '1.13': 4, '1.13.1': 4, '1.13.2': 4,
            '1.14': 4, '1.14.1': 4, '1.14.2': 4, '1.14.3': 4, '1.14.4': 4,
            '1.15': 5, '1.15.1': 5, '1.15.2': 5,
            '1.16': 5, '1.16.1': 5,
            '1.16.2': 6, '1.16.3': 6, '1.16.4': 6, '1.16.5': 6,
            '1.17': 7, '1.17+': 7
        }
        
        if minecraft_version in minecraft_version_to_pack_format:
            self.pack_format = minecraft_version_to_pack_format[minecraft_version]
        else:
            print(f'This version of Minecraft seems to have no pack format defined:\nset to {default_pack_format} by default.')

        self.description = description
        self.author = author

    def __str__(self):
        return str(
            {
                "pack": {
                    "author": self.author,
                    "description": self.description,
                    "pack_format": self.pack_format
                }
            }
        ).replace("'", '"')