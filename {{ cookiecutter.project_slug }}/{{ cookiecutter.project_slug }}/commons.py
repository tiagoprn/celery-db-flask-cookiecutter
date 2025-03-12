import os
import re
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

from sqlalchemy.orm import Query
from sqlalchemy.dialects import postgresql


def get_query_raw_sql(query: Query) -> str:
    """
    Convert a SQLAlchemy query to a readable SQL string with parameters.

    Useful for debugging.
    """
    try:
        # Try with PostgreSQL dialect which handles UUIDs better
        raw_query = str(
            query.statement.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )
    except Exception:
        # Fallback to parameters approach if literal binds fail
        compiled = query.statement.compile()
        params = compiled.params
        raw_query = f"{str(compiled)} [params: {params}]"

    raw_query = re.sub(r"\s+", " ", raw_query).strip()
    return raw_query


def get_version_file_path() -> str:
    root_path = Path().absolute()
    file_path = os.path.join(str(root_path), "VERSION")

    # needed to run the tests, since there it will be
    # on the {{ cookiecutter.project_slug }} package directory,
    # not in the projects' root dir:
    if not os.path.exists(file_path):
        root_path = root_path.parent
        file_path = os.path.join(str(root_path), "VERSION")

    return file_path


@lru_cache(maxsize=None)
def get_app_version():
    file_path = get_version_file_path()
    with open(file_path, "r", encoding="utf-8") as version_file:
        return version_file.read().replace("\n", "")
