script_version = '2.0'
relese_type = 'stable'
latest_supported_config = '2.0'
print('starting...')


def check_update():
    if config['script_updates'] == 'disabled':
        return
    url = 'https://raw.githubusercontent.com/gmankab/backupper/main/latest_release/backupper.py'
    script_b = r.urlopen(url).read()
    script = script_b.decode("utf8")
    begin = script.find("'") + 1
    end = script.find("'", begin)
    new_version = script[begin:end]
    if new_version <= script_version:
        return
    print(f'found new script version: {new_version}')
    if config['script_updates'] == 'ask':
        answer = ''
        while answer not in [
            'y',
            'n',
        ]:
            print('wanna update? y/n')
            answer = input().lower()
        if answer == 'n':
            return
    print('updating...')
    open(__file__, 'wb').write(script_b)
    print()
    print('done, restartind!')
    print()
    restart()


import sys


sys.path.append(
    f'{__file__}/..'
)

from init import config_create
import rich


rich.pretty.install()
config = config_create(
    latest_supported_config,
    script_version,
)





import bot


print(f'started bot v{script_version}')
bot.main()