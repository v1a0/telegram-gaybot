from aiogram import types
from misc import dp
from aiogram.types import Message
from db.prepares import add_or_update_user
from db import insert
from db import remove
from db import select
from db import update
from classes import Branch
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from random import choice
from time import time
from messages import MESSAGES as MSG
from settings import PM
from other import shorter

buffer = []
temp_msg_id = 0


@dp.message_handler(state='*', commands=['s', 'ship', 'shipping'])
async def add_bw(message: types.Message):
    time_to_shipp = (select.last_shippers_time(message.chat.id) + 46400) #66400
    timeout = int(time_to_shipp - time())

    if timeout <= 0:
        await ship(message)

    else:
        await non_ship(message, time_=timeout)


async def ship(message: types.Message):
    add_or_update_user(message, karma_bonus=0.1)
    mems = select.members_and_karma(message.chat.id)

    if not isinstance(mems[0], list):
        await message.reply(MSG.get('not_enough_users'))
        return

    tickets = []

    print(mems)

    for mem in mems:
        for karma in range(int(mem[2])):
            tickets.append(mem[0])

    first = choice(tickets)
    second = choice(tickets)

    while first == second:
        second = choice(tickets)

    remove.shippers(message.chat.id)
    insert.shippers(message.chat.id, first, second, time())

    await message.reply(
        f"♥♥♥♥ {MSG.get('ship_success')} ♥♥♥♥\n"
        f"[{shorter.name(select.name(first))}](tg://user?id={first})"
        f" {MSG.get('and')} "
        f"[{shorter.name(select.name(second))}](tg://user?id={second})\n"
        f"\n"
        f"{MSG.get('nice_day')}\n\n"
        f"{MSG.get('next_ship')}",
        parse_mode=PM
    )

    ship_c_1 = select.ship_count(message.chat.id, first)
    ship_c_2 = select.ship_count(message.chat.id, second)

    print(ship_c_1, ship_c_2)

    if len(ship_c_1) == 0:
        ship_c_1 = [0]

        insert.ship_count(
            group_id=message.chat.id,
            user_id=first,
        )

    if len(ship_c_2) == 0:
        ship_c_2 = [0]

        insert.ship_count(
            group_id=message.chat.id,
            user_id=second,
        )

    ship_c_1 = int(ship_c_1[0])
    ship_c_2 = int(ship_c_2[0])

    update.ship_count(
        group_id=message.chat.id,
        user_id=first,
        value=ship_c_1 + 1
    )

    update.ship_count(
        group_id=message.chat.id,
        user_id=second,
        value=ship_c_2 + 1
    )


async def non_ship(message: types.Message, time_: float):
    add_or_update_user(message)
    seconds = int(time_) % 60
    minutes = int(time_) // 60 % 60
    hours = (int(time_) // 60) // 60

    shippers = select.shippers(message.chat.id)

    await message.reply(

        f"♥♥♥♥ {MSG.get('ship_success')} ♥♥♥♥\n"
        f"{shorter.name(select.name(shippers[0]))}"
        f" {MSG.get('and')} "
        f"{shorter.name(select.name(shippers[1]))}\n"
        f"\n"
        f"{MSG.get('ship_fail_1')}:\n"
        f"{'🕐🕒🕓🕔🕕🕖🕗🕘🕙🕛'[seconds % 10]} "
        f"{hours} {MSG.get('hor')} "
        f"{minutes} {MSG.get('min')} "
        f"{seconds} {MSG.get('sec')} "
        f"{'🕐🕒🕓🕔🕕🕖🕗🕘🕙🕛'[seconds % 10]} "
        # New shipping will be available after 10 seconds
    )


