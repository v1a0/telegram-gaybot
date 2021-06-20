from db import db


def user(user_id: int, username: str):
    db.replace(
        TABLE='users',
        user_id=user_id, username=username
    )
