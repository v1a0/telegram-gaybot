from db import is_exist, insert, select, update, replace
from aiogram.types import Message


def add_or_update_user(message: Message, karma_bonus: float = 0.01):

    if not is_exist.user(message.from_user.id):
        # If this user is unknown or new

        insert.user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            name=message.from_user.first_name
        )
        insert.member(
            user_id=message.from_user.id,
            group_id=message.chat.id
        )
        insert.balance(
            user_id=message.from_user.id,
            balance=0,
        )
        insert.karma(
            user_id=message.from_user.id,
            value=1
        )
        insert.ship_count(
            group_id=message.chat.id,
            user_id=message.from_user.id,
        )

    else:
        # If user already exist, update their data

        update.user(
            user_id=message.from_user.id,
            username=message.from_user.username
        )

        if not is_exist.member(user_id=message.from_user.id, group_id=message.chat.id):
            insert.member(
                user_id=message.from_user.id,
                group_id=message.chat.id
            )

        karma = select.karma(user_id=message.from_user.id)

        if not karma:
            insert.karma(
                user_id=message.from_user.id,
                value=1
            )
        else:
            karma = karma[0] + karma_bonus - karma[0]*0.001
            update.karma(user_id=message.from_user.id, value=karma)

        count = select.ship_count(
            group_id=message.chat.id,
            user_id=message.from_user.id
        )

        if not count:
            insert.ship_count(
                group_id=message.chat.id,
                user_id=message.from_user.id,
            )
