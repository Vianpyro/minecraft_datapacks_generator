import os
from shutil import rmtree
from time import time

class Datapack:
    def __init__(self, title, author="Vianpyro's datapack generator", pack_meta=None, content=None):
        """
        title: The title of the datapack.
        author: The author of the datapack.
        pack_meta: The content of the "pack.mcmeta".
        content: The code the user writes in their datapack.
        """
        # Is this datapack new?
        self.exists = os.path.exists(title)
        self.replace = False

        if self.exists:
            self.replace = input(f'{title} already exists, do you want to replace it? [yes/no]: ')[0].lower() == 'y'

        # Check if datapack format is correct.
        if not isinstance(title, str):
            raise TypeError(f'Argument "title" must be of type "str" not {type(title)}!')

        if not isinstance(author, str):
            raise TypeError(f'Argument "author" must be of type "str" not {type(author)}!')

        if pack_meta is not None and not isinstance(pack_meta, dict):
            raise TypeError(f'Argument "meta" must be of type "dict" not {type(pack_meta)}!')

        elif content is not None and not isinstance(content, dict):
            raise TypeError(f'Argument "content" must be of type "dict" not {type(content)}!')
        

        '''
        Save the title to lower case because of Minecraft datapack structure requiering lower case characters
        Save the subfolder without spaces in between words to recall the functions easier
        '''
        self.title = title.lower()
        self.subfolder_title = self.title.replace(' ', '_')
        self.author = author
        self.pack_meta = pack_meta
        self.content = content
    
    def make_directory(self, name, path=''):
        # Create a directory.
        try:
            os.mkdir(f'{path}{name}')
        except OSError:
            print(f'Failed to create the directory {name}.')
        else:
            print(f'Successfuly created the directory {name}.')
    
    def create_file(self, name, path='', content=''):
        # Create a file.
        with open(f'{path}{name}', 'w') as f:
            if isinstance(content, str):
                f.write(content)
            elif isinstance(content, list):
                for line in content:
                    f.write(f'{line}\n')
            else:
                raise TypeError(f'Argument "content" must be of type "str" or "list" not {type(content)}!')
            f.close()

    def compile(self):
        '''
        Function to translate the Python code into a Minecraft datapack
        Probably the most important function of this program
        '''
        # Removing or not the older datapack with the same name (if it exists)
        if self.exists:
            if not self.replace:
                raise ValueError('Could not replace previous datapack.')
            else:
                try:
                    rmtree(self.title)
                except:
                    print(f'Failed to delete the directory {self.title}.')
                else:
                    print(f'Successfuly deleted the directory {self.title}.')

        # Starting the translation into the datapack
        print('Generating the datapack, this might take a few seconds...')
        time_stamp = time()

        if not self.exists or self.replace:
            # Create the datapack directory
            self.make_directory(self.title)

            # Create the "pack.mcmeta" file
            if self.pack_meta == None:
                print('No "pack.mcmeta" was generated!')
            else:
                self.create_file(
                    'pack.mcmeta', f'{self.title}/',
                    str(Pack(
                        self.pack_meta['minecraft_version'],
                        self.pack_meta['description'],
                        self.author
                    ))
                )

            if self.content == None:
                print('No content was generated!')
            else:
                # Create the data directory containing every modification brung by the datapack
                self.make_directory('data', f'{self.title}/')
                self.make_directory(self.subfolder_title, f'{self.title}/data/')

                for key in self.content:
                    directory_name = f'{self.title}/data/{self.subfolder_title}/{key}/'
                    
                    if key in ['functions', 'predicates'] and self.content[key] is not None:
                        # Create the key folder
                        print(f'Generating {key} files...')
                        self.make_directory(directory_name)
                        
                        if key == 'functions':
                            for function_file in self.content[key]:
                                self.create_file(
                                    f'{function_file}.mcfunction', directory_name,
                                    self.content[key][function_file]
                                )
                        elif key == 'predicates':
                            pass

                        print(f'Successfuly generated {key} files.')
                    elif self.content[key] is None:
                        print(f'No file was generated for "{key}".')
                    else:
                        print(f'Failed to create {key} files : {key} is not supported (yet?).')
                    
        print(f'Successfuly generated the datapack in {time() - time_stamp:0.1} seconds :).')


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
            print(
                f'This version of Minecraft seems to have no pack format defined:\nset to {default_pack_format} by default.')

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


def mcfunction(directory):
    try:
        with open(f'{directory}.mcfunction', 'r') as f:
            r = [line.replace('\n', '') for line in f if line not in ['', ' ', '\n']]
            f.close()
        return r
    except:
        raise ValueError(f'Could not read the file {directory}')


assert Datapack('TeSt tItLe').title == 'test title'
