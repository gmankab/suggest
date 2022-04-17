from pathlib import Path
import shutil
import stat
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
        Path(file).resolve().parent
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


def get_username(user):
    if user.username:
        return user.username
    else:
        return user.id


def auto_rename(file):
    file = Path(file)
    ls = os.listdir(file.parent)
    count = 0
    new_name = file.name
    while new_name in ls:
        count += 1
        new_name = f'{file.stem}{count}{file.suffix}'
    os.rename(file, new_name)
    return clean_path(Path(file.parent, new_name))


def restart(*args):
    command = f'{sys.executable} {Path(__file__)} {" ".join(args)}'
    globals().clear()
    import os as new_os
    import sys as new_sys
    new_os.system(command)
    new_sys.exit()


def rmtree(dir):
    try:
        for root, dirs, files in os.walk(
            dir,
            topdown=False,
        ):
            for name in files:
                filename = os.path.join(
                    root,
                    name,
                )
                os.chmod(
                    filename,
                    stat.S_IWUSR,
                )
                os.remove(filename)
            for name in dirs:
                os.rmdir(
                    os.path.join(
                        root,
                        name,
                    )
                )
    except PermissionError as error:
        raise PermissionError(
            f'Can\'t remove dir "{dir}", no permissions. Try to remove it yourself'
        ) from error