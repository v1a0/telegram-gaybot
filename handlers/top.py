from aiogram import types
from misc import dp
from aiogram.types import Message
from settings import PM
from db.prepares import add_or_update_user
from db import select
import re
from other import shorter
from messages import MESSAGES as MSG


@dp.message_handler(state='*', commands=['top', 't'])
async def topping(message: types.Message):
    add_or_update_user(message)
    await top_gays(message)


@dp.message_handler(state='*', regexp=r'/top\d{1,3}')
async def topping(message: types.Message):
    add_or_update_user(message)
    limit = re.findall(r'\d{1,3}', message.text)[0]
    await top_gays(message, limit=limit)


async def top_gays(message: Message, limit: int = 10):
    top_list = select.members_and_balance(group_id=message.chat.id, limit=limit)
    msg = MSG.get('gay_top') + '\n\n'

    emojis = [
        '🏳️‍🌈',
        '🍑',
        '🔥',
        '🍩',
        '🌝',
        '🇩🇪', '🦄'
    ]

    if not isinstance(top_list[0], list):
        top_list = [top_list]

    for topper in top_list:
        position = top_list.index(topper) + 1
        name = select.name(topper[0])
        balance = topper[1]

        name = shorter.name(name)

        msg += f'{position} ' \
               f'{"" if not emojis else emojis.pop(0)} ' \
               f'{name}: {balance} GC ' \
               f'\n\n'
        # f'[{name}](tg://user?id={username}): {balance} GC ' \

    await message.reply(
        msg,
        parse_mode=PM
    )


@dp.message_handler(state='*', commands=['ship_top', 'st'])
async def topping(message: types.Message):
    add_or_update_user(message)
    await ship_top(message)


@dp.message_handler(state='*', regexp=r'/ship_top\d{1,3}')
async def topping(message: types.Message):
    add_or_update_user(message)
    limit = re.findall(r'\d{1,3}', message.text)[0]
    await ship_top(message, limit=limit)


async def ship_top(message: Message, limit: int = 10):
    top_list = select.ship_count_all(group_id=message.chat.id, limit=limit)
    msg = MSG.get('ship_top') + '\n\n'

    emojis = [
        '🥇',
        '🥈',
        '🥉',
    ]

    if not isinstance(top_list[0], list):
        top_list = [top_list]

    for topper in top_list:
        position = top_list.index(topper) + 1
        user_id = topper[0]
        count = topper[1]
        name = shorter.name(select.name(user_id))

        msg += f'{position if not emojis else emojis.pop(0)} : ' \
               f'{name} ' \
               f'({count} ship.)' \
               f'\n\n'

    await message.reply(
        msg,
        parse_mode=PM,
        reply=False
    )
