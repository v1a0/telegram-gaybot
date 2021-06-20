from db import db


def member(group_id: int, user_id: int) -> bool:
    return bool(db.select(
        SELECT='user_id',
        TABLE='members',
        WHERE={
            'group_id': group_id,
            'user_id': user_id
        }
    ))


def user(user_id: int) -> bool:
    return bool(db.select(
        SELECT='username',
        TABLE='users',
        WHERE={
            'user_id': user_id
        }
    ))

