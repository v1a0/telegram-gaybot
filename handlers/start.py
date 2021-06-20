from misc import dp
from classes import Branch
from aiogram import types
from messages import MESSAGES
from settings import BAN_LIST
from db.prepares import add_or_update_user


@dp.message_handler(state=Branch.banned)
async def start(message: types.Message):
    return


@dp.message_handler(state='*', commands=['start', 'about'])
async def start(message: types.Message):
    add_or_update_user(message)

    if message.from_user.id in BAN_LIST:
        await Branch.banned.set()
        await message.reply(MESSAGES['banned'])

    await message.reply(MESSAGES['about'], reply=False)




