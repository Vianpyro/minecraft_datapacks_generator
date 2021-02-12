from pack import Pack
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
            print(f'Creation of the directory {name} failed.')
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

        print('Generating the datapack, this might take a few seconds...')
        time_stamp = time()

        # Generate the datapack.
        if self.exists and not self.replace:
            raise Warning(f'Could not write {self.title}!')
        else:
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
                    print(f'Generating {key} files...')
                    directory_name = f'{self.title}/data/{self.subfolder_title}/{key}/'
                    
                    if key == 'functions':
                        self.make_directory(directory_name)

                        for function_file in self.content[key]:
                            self.create_file(
                                f'{function_file}.mcfunction', directory_name,
                                self.content[key][function_file]
                            )
                        print(f'Successfuly generated {key} files.')
                    else:
                        print(f'{key} files are not supported (yet?).')


        print(f'Successfuly generated the datapack in {time() - time_stamp:0.1} seconds :).')


def mcfunction(directory):
    try:
        with open(directory, 'r') as f:
            r = [line.replace('\n', '') for line in f]
            f.close()
        return r
    except:
        raise ValueError(f'Could not read the file {directory}')


assert Datapack('TeSt tItLe').title == 'test title'
