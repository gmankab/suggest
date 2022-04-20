script_version = '2.0'
relese_type = 'stable'
latest_supported_config = '2.0'
print('starting...')


from stat import filemode
import sys
import os
from urllib import request as r
from pathlib import Path


def check_update():
    def restart():
        command = f'{sys.executable} {sys.argv[0]}'
        globals().clear()
        import os as new_os
        import sys as new_sys
        new_os.system(command)
        new_sys.exit()

    def get_bytes(url):
        return r.urlopen(url).read()

    def rewrite(
        file,
        bytes,
    ):
        file = Path(file).resolve()
        print(f'updating {file}')
        open(file, 'wb').write(bytes)
        print('done')

    urls = (
        'https://raw.githubusercontent.com/gmankab/suggest/main/latest_release/init.py',
        'https://raw.githubusercontent.com/gmankab/suggest/main/latest_release/func.py',
        'https://raw.githubusercontent.com/gmankab/suggest/main/latest_release/bot.py',
    )
    main_b = get_bytes('https://raw.githubusercontent.com/gmankab/suggest/main/latest_release/suggest.py')
    main_text = main_b.decode("utf8")
    begin = main_text.find("'") + 1
    end = main_text.find("'", begin)
    new_version = main_text[begin:end]
    if new_version > script_version:
        rewrite(
            __file__,
            main_b,
        )
        for url in urls:
            filename = url.rsplit('/', 1)[-1]
            file = f'{__file__}/../{filename}'
            rewrite(
                file,
                get_bytes(
                    url
                )
            )
        print('done, restartind!')
        restart()
    for url in urls:
        filename = url.rsplit('/', 1)[-1]
        file = f'{__file__}/../{filename}'
        if not Path(file).exists():
            rewrite(
                file,
                get_bytes(
                    url
                )
            )


check_update()


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
