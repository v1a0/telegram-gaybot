from db import db
from sqllex.constants import IGNORE, NULL


def user(user_id: int, username: str):
    db.update(
        TABLE='users',
        SET={
            'username': username
        },
        WHERE={
            'user_id': user_id,
        }
    )


def balance(user_id: int, balance: int):
    db.update(
        TABLE='coins',
        SET={
            'balance': balance
        },
        WHERE={
            'user_id': user_id,
        }
    )


def karma(user_id: int, value: int):
    db.update(
        TABLE='karma',
        SET={'karma': value},
        WHERE={'user_id': user_id}
    )


def ship_count(group_id, user_id: int, value: int):
    db.update(
        TABLE='ship_count',
        SET={'count': value},
        WHERE={'group_id': group_id, 'user_id': user_id}
    )


def custom_name(user_id: int, new_name: str):
    if new_name == 'default':
        new_name = ''

    db.update(
        TABLE='users',
        SET={
            'custom_name': new_name
        },
        WHERE={
            'user_id': user_id,
        }
    )
