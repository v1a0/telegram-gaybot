from aiogram import types
from misc import dp
from aiogram.types import Message
from settings import PM
from db.prepares import add_or_update_user
from db import update, select
import re
from other import shorter
from messages import MESSAGES as MSG


@dp.message_handler(state='*', commands=['name', 'rename', 'call'])
async def topping(message: types.Message):
    add_or_update_user(message)

    if not (message.from_user.id in select.admins_ids()) and (message.reply_to_message.from_user.id != message.from_user.id):
        await message.reply(
            f"{MSG.get('permission_denied')}. {MSG.get('change_your_nick')}"
        )
        return

    await custom_name(message)


async def custom_name(message: types.Message):
    name = message.text.split()[1:]
    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        user_id = message.from_user.id

    name = ' '.join(word for word in name)

    if not name:
        return await message.reply(
            f"Enter nickname you wish to set after '/name'\nFor example:\n`/name Alis`",
            parse_mode=PM
        )

    update.custom_name(user_id=user_id, new_name=name)

    await message.reply(
        f"{MSG.get('name_changed_to')[0]} "
        f"@{select.username(user_id)[0]} "
        f"{MSG.get('name_changed_to')[1]} "
        f'''{'"' if name != 'default' else ''}'''
        f'{name}'
        f'''{'"' if name != 'default' else ''}'''
    )

