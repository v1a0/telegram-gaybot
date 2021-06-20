from sqllex import *
from db import db


def balance(user_id: int):
    return db.select(
        TABLE='coins',
        SELECT='balance',
        WHERE={
            'user_id': user_id
        }
    )[0]


def balances(limit: int = 10):
    return db.select(
        TABLE='coins',
        LIMIT=limit,
        ORDER_BY='balance DESC'
    )


def members(group_id: int, limit: int = 10):
    return db.select(
        TABLE='members',
        SELECT='user_id',
        WHERE={
            'group_id': group_id
        },
        LIMIT=limit,
    )


def username(user_id: int):
    return db.select(
        TABLE='users',
        SELECT='username',
        WHERE={
            'user_id': user_id
        }
    )


def name(user_id: int):
    custom = db.select(
        TABLE='users',
        SELECT='custom_name',
        WHERE={
            'user_id': user_id
        }
    )

    if custom[0]:
        return custom[0] #?

    return db.select(
        TABLE='users',
        SELECT='name',
        WHERE={
            'user_id': user_id
        }
    )[0]


def karma(user_id: int) -> list:
    return db.select(
        SELECT='karma',
        TABLE='karma',
        WHERE={'user_id': user_id}
    )


def xwords() -> list:
    return db.select(
        TABLE='xwords',
        SELECT='word'
    )


def is_xword(word: str) -> bool:
    return bool(db.select(
        TABLE='xwords',
        SELECT='id',
        WHERE=f"word like '%{word}%'"
    ))


def members_and_balance(group_id: int, limit: int = 10, order_by: str = 'co.balance DESC') -> list:
    return db.select(
        SELECT=['co.user_id', 'balance'],
        FROM=['users', AS, 'us'],  # FROM users AS us
        JOIN=[  # JOIN
            ['members', AS, 'mem', ON, f'mem.user_id == us.user_id AND mem.group_id == {int(group_id)}'],
            [CROSS_JOIN, 'coins', AS, 'co', ON, 'co.user_id == us.user_id'],
        ],
        ORDER_BY=order_by,  # order by age ASC
        LIMIT=limit,
    )


def admins_ids() -> list:
    return db.select(
        SELECT='user_id',
        FROM='users',
        WHERE={'admin': 'True'}
    )


def admins() -> list:
    return db.select(
        SELECT=['name'],
        FROM='users',
        WHERE={'admin': 'True'}
    )


def members_and_karma(group_id: int, limit: int = 100, order_by: str = 'karma DESC') -> list:
    return db.select(
        SELECT=['ka.user_id', 'name', 'karma'],
        FROM=['karma', AS, 'ka'],  # FROM users AS us
        JOIN=[  # JOIN
            ['members', AS, 'mem', ON, f'mem.user_id == us.user_id AND mem.group_id == {int(group_id)}'],
            [CROSS_JOIN, 'users', AS, 'us', ON, 'us.user_id == ka.user_id'],
        ],
        ORDER_BY=order_by,  # order by age ASC
        LIMIT=limit,
    )


def last_shippers_time(group_id):
    r = db.select(
        SELECT='time',
        FROM='shippers',
        WHERE={'group_id': group_id}
    )

    if not r:
        r = 0
    else:
        r = r[0]

    return float(r)


def shippers(group_id, limit: int = 100):
    return db.select(
        SELECT=['id_first', 'id_scond'],
        TABLE='shippers',
        WHERE={"group_id": group_id},
        LIMIT=limit
    )


def ship_count(group_id, user_id: int):
    return db.select(
        SELECT='count',
        TABLE='ship_count',
        WHERE={
            'group_id': group_id,
            'user_id': user_id
        },
        ORDER_BY='count DESC'
    )


def ship_count_all(group_id: int, limit: int = 100):
    return db.select(
        SELECT=['user_id', 'count'],
        TABLE='ship_count',
        WHERE={
            'group_id': group_id,
        },
        ORDER_BY='count DESC',
        LIMIT=limit
    )
