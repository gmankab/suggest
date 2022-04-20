from urllib import request as r
from inspect import cleandoc as cd
from pathlib import Path
import func as f
import subprocess
import traceback
import asyncio
import shutil
import sys
import os


def config_create(
    latest_supported_config = None,
    script_version = None,
):
    blank_config = f"""\
# # # please reset all "_" with your values. All values must be specified without quotes.

# # # BOT TOKEN
# # # open https://t.me/BotFather, create bot and copy bot token
bot_token: _

# # # API KEY
# # # Open https://my.telegram.org/apps and copy api_id and api_hash.
# # # WARNING: use ony your own api_id and api_hash. I already tried to take them from decompiled official telegram app, and 20 minutes later my telegram account get banned. Then I wrote email with explanation on recover@telegram.org and on the next day and they unbanned me. So please use only your own api_id and api_hash.
# # # Why is the API key needed for bots? Answer: https://docs.pyrogram.org/faq/why-is-the-api-key-needed-for-bots

api_id: _
api_hash: _

# # # example:
# api_id: 12345
# api_hash: 0123456789abcdef0123456789abcdef


# # # CHATS
# You can find ID of any chat in your browser's address bar at https://web.telegram.org/z/. It must be number without letters.
# WARNING: if ID have "-" sign at the beginning then you must add "100" after "-". For example, you must use "-100154636" instead of "-154636". Also if it hasn't "-" sign then you don't need to touch it. For example, it can be "38523532", "1348592", or "-100954843". If you want to use your account's "saved messages", input "me". Or you can use @name, of any user, chanel or chat

# # # id of the chat in which confirmed suggestions will be published
main_chat: _

# # # id of the chat in which you will confirm suggestions
# confirming_chat: -703744909

# database_log_chat: -607362670
# bugreport_chat:


# # # WARNING: DON'T TOUCH VERSION
# # # WARNING: DON'T TOUCH VERSION
version: {script_version}  # # # WARNING: DON'T TOUCH VERSION
# # # WARNING: DON'T TOUCH VERSION
# # # WARNING: DON'T TOUCH VERSION
"""

    def new():
        config_load(blank_config)
        config_dump()
        console.print(f'Created new config: {config_path}, please check, read and fill it. You can close this script for now and open it later, after filling config. Or don\'t close it and just press Enter after filling config to continue', style = 'light_green')
        input()
        config_load()

    if (
        Path(config_path).exists()
    ) and (
        os.stat(config_path).st_size != 0
    ):
        config_load()
        if latest_supported_config and script_version:
            if (
                'version' not in config
            ) or (
                str(config['version']) < latest_supported_config
            ) or (
                str(config['version']) > script_version
            ):
                console.print(f'[red]old[/red] {config_path} [red]file renamed to[/red] {f.auto_rename(config_path)}')
                new()
    else:
        new()

    while '_' in config.values():
        for key, val in config.items():
            if val == '_':
                console.print(
                    f'[bright_red]please specify value for[/bright_red] {key} [bright_red]in config'
                )
        console.print(f'your config path - [purple]{config_path}')
        input('press enter to continue')
        config_load()
    return config


def install_libs():
    print('installing libs')
    requirements = [
        'rich',
        'psutil',
        'pyrogram',
        'tgcrypto',
        'ruamel.yaml',
        'python-dateutil',
    ]

    pip = f'{sys.executable} -m pip'
    pip_chache = f'{downloads}/pip_chache'
    output = subprocess.getstatusoutput(
        f'{pip} install --upgrade pip'
    )[1]
    print(output)
    if 'No module named pip' in output:
        print('installing pip...')
        # pip is a shit which allow to install libs, so if we want to install libs we must have pip
        py_dir = f.get_parrent_dir(sys.executable)

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
        f.mkdir(downloads)

        r.urlretrieve(
            url = 'https://bootstrap.pypa.io/get-pip.py',
            filename = get_pip,
        )
        os.system(f'{sys.executable} {get_pip} --no-warn-script-location')
        os.remove(get_pip)

    if Path(libs_dir).exists():
        print(f'deleting {libs_dir}')
        # f.rmtree(libs_dir)
    os.system(f'{pip} config set global.no-warn-script-location true')
    os.system(f'{pip} install -U {" ".join(requirements)} -t {libs_dir} --cache-dir {pip_chache}')


def config_load(
    data = None
):
    global config
    if data:
        config = yml.load(
            data
        ) or {}
    else:
        config = yml.load(
            open(
                config_path,
                'r'
            ).read()
        ) or {}


def config_dump(
    data = None
):
    if not data:
        data = config
    yml.dump(
        data,
        open(
            config_path,
            'w',
        ),
    )


cwd = f'{f.get_parrent_dir(__file__)}/data'
config_path = f'{cwd}/config.yml'
downloads = f'{cwd}/downloads'
libs_dir = f'{cwd}/libs'

f.mkdir(cwd)
config = {}


# adding libs and files from Current Work Dir to sys.path
# this is needed so that python can find this libs and files, then use them
sys.path += (
    cwd,
    libs_dir,
)


try:
    from dateutil.relativedelta import relativedelta
    import ruamel.yaml
    import pyrogram
    import psutil

    # this lib needed for beautiful output:
    import rich
    from rich import pretty
except ImportError as import_error:
    print(import_error)
    install_libs()
    print('restarting')
    f.restart()


filters = pyrogram.filters
Button = pyrogram.types.InlineKeyboardButton
pretty.install()
yml = ruamel.yaml.YAML()
console = rich.console.Console(
    record = True
)
