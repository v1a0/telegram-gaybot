from db import db


def member(group_id: int, user_id: int):
    db.delete(
        TABLE='members',
        WHERE={
            'group_id': group_id,
            'user_id': user_id
        },
    )


def shippers(group_id):
    db.delete(
        TABLE='shippers',
        WHERE={"group_id": group_id}
    )

