from datetime import datetime, timedelta
from typing import List

from {{cookiecutter.project_slug}}.models import User


def create_multi_users():
    created_users = []
    users_data = [
        {
            'username': 'jean_luc_picard',
            'email': 'jlp@startrek.com',
            'password': '12345678',
        },
        {
            'username': 'william_riker',
            'email': 'wk@startrek.com',
            'password': '12345678',
        },
        {'username': 'deanna_troy', 'email': 'dt@startrek.com', 'password': '12345678'},
    ]
    for data in users_data:
        new_user = User().register(**data)
        created_users.append(new_user)
    return created_users
