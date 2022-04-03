'''
A bot that allows you to suggest posts in telegram channels, as in VK publics
python 3.10.4
'''

# importing libraries
from urllib import request as r
from inspect import cleandoc as cd
import subprocess
import traceback
import pathlib
import shutil
import sys
import os


def clean_path(path):
    path = str(path).replace('\\', '/')
    # conerting a\\b///\\\c\\/d/e/ to a//b//////c///d/e/

    # conerting a//b//////c///d/e/ to a/b/c/d/e/
    while '//' in path:
        path = path.replace('//', '/')
    return path


def get_parrent_dir(file):
    return clean_path(
        pathlib.Path(file).parent
    )


def mkdir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def clear_dir(dir):
    shutil.rmtree(
        dir,
        ignore_errors=True,
    )
    mkdir(dir)


# changing current work dir
cwd = f'{get_parrent_dir(__file__)}/data'
mkdir(cwd)
os.chdir(cwd)

downloads = f'{cwd}/downloads'
libs = f'{cwd}/libs'

# adding libs and files from Current Work Dir to sys.path
# this is needed so that python can find this libs and files, then use them

sys.path += (
    cwd,
    libs,
)

if len(sys.argv) > 1:
    config_path = sys.argv[1]
else:
    config_path = f'{cwd}/config.yml'


def install_libs():
    print('checking if all libs installed...')
    pip = f'{sys.executable} -m pip'

    requirements = [
        'rich',
        'pyrogram',
        'tgcrypto',
        'ruamel.yaml'
    ]

    try:
        for requirement in requirements:
            __import__(requirement)
    except ImportError as import_error:
        print(import_error)
        print('deleating pip chache')
        output = subprocess.getstatusoutput(
            f'{pip} cache purge'
        )[1]
        print(output)
        if 'No module named pip' in output:
            print('installing pip...')
            # pip is a shit which allow to install libs, so if we want to install libs we must have pip
            py_dir = get_parrent_dir(sys.executable)

            # fixing shit which doesn't allow to install pip in python embedable in windows:
            for file in os.listdir(
                py_dir
            ):
                if file[-5:] == '._pth':
                    with open(
                        f'{py_dir}/{file}', 'r+'
                    ) as file:
                        if '#import site' in file.readlines()[-1]:
                            file.write('import site')

            # instaling pip:
            get_pip = f'{downloads}/get-pip.py'
            clear_dir(downloads)

            r.urlretrieve(
                url = 'https://bootstrap.pypa.io/get-pip.py',
                filename = get_pip,
            )
            os.system(f'{sys.executable} {get_pip} --no-warn-script-location')

        os.system(f'{pip} config set global.no-warn-script-location true')
        os.system(f'{pip} install -U pip {" ".join(requirements)} -t {libs}')
        print('installed, restarting...')
        os.system(f'{sys.executable} {pathlib.Path(__file__)}')
        sys.exit()


install_libs()


import pyrogram
import ruamel.yaml

# this lib needed for beautiful output:
import rich
from rich import pretty


pretty.install()
print = rich.console.Console().print
yml = ruamel.yaml.YAML()
config = {}


if not os.path.isfile(config_path):
    open(config_path, 'w').close()


def load_config():
    global config
    config = yml.load(
        open(config_path, 'r')
    ) or {}  # empty dict if config file empty


load_config()


def dump_config():
    open(config_path, 'w').write(
f'''
# please open https://t.me/BotFather, create bot and copy bot token
token: {config['token']}

'''
    )


tg = pyrogram.Client(
    bot_token = config['bot_token']
)
