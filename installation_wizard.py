# -*- coding:utf-8 -*-
from json import loads
import os
from time import time
import urllib.request as dlurl
from zipfile import ZipFile

# Save the name of the directory and the path to it into variables
directory = 'minecraft_datapacks_generator'
folder = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\Python\\Python39\\Lib' if os.name == 'nt' else '/usr/lib/python3.9'
exist = os.path.exists(f'{folder}\\{directory}') and os.path.isdir(f'{folder}\\{directory}')

def ask_user(querry):
    return input(f'{querry}? [yes/no]: ')[0].lower() == 'y'

# Scan the user computer
if exist:
    print(f'Found at: {folder}\\{directory}, replace this version with the latest release.')
else:
    print('Unable to find the library.')
    if ask_user('Do you want to scan your computer to look for the folder'):
        found = False
        directory_list = str(folder + '\\site-packages').split('\\')
        tree = ['\\'.join(directory_list[:i + 1]) for i in range(len(directory_list))][::-1]

        try:
            time0 = time()
            HDDs = tree + [e + ':\\' for e in 'CDEFGHIJK' if os.path.exists(e + ':\\')]

            for HDD in HDDs:
                if not found:
                    for path, dirs, files in os.walk(HDD):
                        if folder + '\\' + directory in path:
                            found = True
                            print(f'Found at: {path} in {time() - time0:0.1} seconds.')
                            break
        except OSError as e:
            print(e)
        else:
            print(f'Paste the "minecraft_datapack_generator" folder in here: {folder}\\{directory}.')

# Download the latest version
try:
    resp = dlurl.urlopen(f'https://api.github.com/repos/Vianpyro/{directory}/releases')
    data = loads(resp.read())[0]
    version = data['tag_name']

    if ask_user(f'Would you like to download the latest version ({version})'):
        try:
            print(f'Downloading {directory} {version}...')
            dlurl.urlretrieve(f'https://github.com/Vianpyro/{directory}/archive/{version}.zip', f'{directory}.zip')
            print(f'Successfully downloaded {directory} {version}.')

            print(f'Unziping {directory} {version}...')
            with ZipFile(f'{directory}.zip', 'r') as zipf:
                zipf.extractall(f'{folder}')
                zipf.close()
                os.remove(f'{directory}.zip')
                if exist:
                    print(
                        f'Successfully extracted {directory} {version} in "{folder}".',
                        f'\nYou now have to delete the old version of the library and rename the most recent one "{directory}".'
                    )
                else:
                    os.rename(f'{folder}\\{directory}-{version}', f'{folder}\\{directory}')
                    print(f'Successfully extracted and installed {directory} {version} in "{folder}".')
        except:
            print(f'Unable to download and/or extract "https://github.com/Vianpyro/{directory}/archive/{version}.zip"')
except:
    print('Unable to resolve host name.')

input('Press "enter" to close this window.')