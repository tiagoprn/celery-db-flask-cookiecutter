import os
from functools import lru_cache
from pathlib import Path


def get_version_file_path() -> str:
    root_path = Path().absolute()
    file_path = os.path.join(str(root_path), 'VERSION')

    # needed to run the tests, since there it will be
    # on the {{ cookiecutter.project_slug }} package directory,
    # not in the projects' root dir:
    if not os.path.exists(file_path):
        root_path = root_path.parent
        file_path = os.path.join(str(root_path), 'VERSION')

    return file_path


@lru_cache(maxsize=None)
def get_app_version():
    file_path = get_version_file_path()
    with open(file_path, 'r', encoding='utf-8') as version_file:
        return version_file.read().replace('\n', '')
