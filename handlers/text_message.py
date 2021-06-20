from misc import dp
from classes import Branch
from aiogram.types import ContentTypes, Message
from db.select import xwords
from settings import PM
from db.prepares import add_or_update_user
from db import update, select


@dp.message_handler(state='*', content_types=ContentTypes.TEXT)
async def any_message(message: Message):
    add_or_update_user(message)

    await bad_words_search(message)


async def bad_words_search(message: Message):
    coins = 0
    msg_no_spaces = message.text.replace(' ', '')

    for word in xwords():
        coins += msg_no_spaces.lower().count(word)

    if coins:
        if coins > 25:
            coins = 25

        await message.reply(
            f'@{message.from_user.username} '
            f'got '
            f'{coins} '
            f'GayCoin'
            f'{"s" if coins > 1 else ""}',
        )

        balance = select.balance(user_id=message.from_user.id)

        update.balance(
            user_id=message.from_user.id,
            balance=balance+coins
        )

