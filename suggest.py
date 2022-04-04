'''
I am a bot who allows you to suggest posts in telegram channels, as in VK publics
python 3.10.4
'''

# importing libraries
from urllib import request as r
from inspect import cleandoc as cd
import subprocess
import traceback
import asyncio
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
        clear_dir(downloads)
        print('installed, restarting...')
        os.system(f'{sys.executable} {pathlib.Path(__file__)}')
        sys.exit()
    print('done')


install_libs()


import pyrogram
from pyrogram import filters
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
f'''\
# please open https://t.me/BotFather, create bot and copy bot token
token: {config['token']}

# please open https://my.telegram.org/apps and copy api_id and api_hash.
# WARNING: use ony your own api_id and api_hash. I already tried to take them from decompiled official telegram app, and 20 minutes later my telegram account get banned. Then I wrote email with explanation on recover@telegram.org and on the next day they unbanned me. So please use only your own api_id and api_hash
api_id: {config['api_id']}
api_hash: {config['api_hash']}

# You can find ID of any chat in your browser's address bar at https://web.telegram.org/z/. It must be number without letters.
# WARNING: if ID have "-" sign at the beginning then you must add "100" after "-". For example, you must use "-100154636" instead of "-154636". Also if it hasn't "-" sign then you don't need to touch it. For example, it can be "38523532", "1348592", or "-100954843". If you want to use your account's "saved messages", input "me". Or you can use @name, of any user, chanel or chat.
channel_id: {config['channel_id']}
'''
    )


def make_config():
    create_new_config = False

    def check_val(
        key: str,
        comment: str,
        val: any = None,
    ):
        nonlocal create_new_config
        if key not in config:
            if not create_new_config:
                create_new_config = True
                print(f'creating new config {config_path}')
            if not val:
                print(
                    comment,
                    end=''
                )
                val = input()
            config[key] = val

    check_val(
        key = 'token',
        comment = 'please open https://t.me/BotFather, create bot and copy bot token, then paste token here >> ',
    )

    if (
        'api_id' not in config
    ) or (
        'api_hash' not in config
    ):
        print('\nplease open https://my.telegram.org/apps and copy api_id and api_hash.\n[bold red]warning[/bold red]: use ony your own api_id and api_hash. I already tried to take them from decompiled official telegram app, and 20 minutes later my telegram account get banned. Then I wrote email with explanation on recover@telegram.org and on the next day they unbanned me. So please use only your own api_id and api_hash\bWhy is the api key needed for bots? Answer - https://docs.pyrogram.org/faq/why-is-the-api-key-needed-for-bots')

    check_val(
        key = 'api_id',
        comment = 'input api_id >> ',
    )

    check_val(
        key = 'api_hash',
        comment = 'input api_hash >> ',
    )

    check_val(
        key = 'channel_id',
        comment = '\nYou can find ID of any chat in your browser\'s address bar at https://web.telegram.org/z/. It must be number without letters.\n[bold red]warning[/bold red]: if ID have "-" sign at the beginning then you must add "100" after "-". For example, you must use "-100154636" instead of "-154636". Also if it hasn\'t "-" sign then you don\'t need to touch it. For example, it can be "38523532", "1348592", or "-100954843". If you want to use your account\'s "saved messages", input "me". Or you can use @name, of any user, chanel or chat.\n\ninput id of the chat in which suggestions that you confirm will be published >>'
    )

    if create_new_config:
        print(
            f'[bright_green]Created new config[/bright_green], please check it: {config_path}',
        )
        dump_config()
        load_config()


make_config()


tg = pyrogram.Client(
    session_name = 'suggest',
    bot_token = config['token'],
    api_id = config['api_id'],
    api_hash = config['api_hash']
)


@tg.on_message(filters.command(['help', 'start']))
async def start_command(app, msg):
    await msg.reply(
        'Hello! Send me any message to suggest it to @example_gmanka_channel'
    )


@tg.on_message()
async def echo(app, msg):
    for admin in await app.get_chat_members(
        chat_id = config['channel_id'],
        filter="administrators"
    ):
        if not admin.user.is_bot:
            print(admin.user.id)
            await msg.forward(admin.user.id)


print('bot started')

tg.run()
