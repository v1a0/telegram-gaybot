from db import db
from typing import Union
from sqllex.constants import REPLACE, IGNORE
from badwords import bad_words_variator


def user(user_id: int, username: str = '', name: str = ''):
    db.insert(
        TABLE='users',
        OR=REPLACE,
        user_id=user_id, username=username, name=name
    )


def karma(user_id: int, value: int):
    db.insert(
        TABLE='karma',
        OR=REPLACE,
        user_id=user_id, karma=value
    )


def member(group_id: int, user_id: int):
    db.insert(
        TABLE='members',
        OR=REPLACE,
        group_id=group_id, user_id=user_id
    )


def balance(user_id: int, balance: int):
    db.insert(
        TABLE='coins',
        OR=REPLACE,
        user_id=user_id, balance=balance
    )


def xwords(words: Union[str, list]):
    if isinstance(words, str):
        words = [words]

    for word in words:
        for _word in bad_words_variator(word):
            db.insert(
                TABLE='xwords',
                OR=IGNORE,
                word=_word
            )


def shippers(group_id, first_id: int, second_id: int, time: float):
    db.insert(
        TABLE='shippers',
        OR=REPLACE,
        group_id=group_id, id_first=first_id, id_scond=second_id, time=time
    )


def ship_count(group_id, user_id: int):
    db.insert(
        TABLE='ship_count',
        OR=REPLACE,
        group_id=group_id, user_id=user_id, count='0'
    )

