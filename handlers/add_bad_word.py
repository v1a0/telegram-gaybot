from aiogram import types
from misc import dp
from aiogram.types import Message
from db.prepares import add_or_update_user
from db import insert
from db.select import admins_ids
from classes import Branch
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

buffer = []
temp_msg_id = 0


@dp.message_handler(state='*', commands=['x', 'xxx', 'add_bad_word'])
async def add_bw(message: types.Message):
    add_or_update_user(message)

    if not (message.from_user.id in admins_ids()):
        return

    await adder(message)


async def adder(message: Message):
    global buffer
    global temp_msg_id
    buffer = message.text.split()[1:]

    if not buffer:
        return

    await Branch.add_xword_response.set()

    msg = f"Are you sure you would like to add new xwords?\n"

    for b in buffer:
        msg += f'{buffer.index(b) + 1}. {b}\n'

    inline_b1 = InlineKeyboardButton('Yes', callback_data=f'y_{message.chat.id}')
    inline_b2 = InlineKeyboardButton('No', callback_data=f'n_{message.chat.id}')
    inline_kb1 = InlineKeyboardMarkup(row_width=2).add(inline_b1, inline_b2)

    temp = await message.reply(
        f"{msg}"
        f"\ny/n",
        reply_markup=inline_kb1
    )

    temp_msg_id = temp.message_id


# @dp.message_handler(state=Branch.add_xword_response)
# async def add_bw(message: types.Message):
#     global buffer
#
#     if not (message.from_user.id in ADMIN_ID):
#         return
#
#     if message.text.lower() in ['y', 'yes', 'ye', 'yup']:
#         insert.xwords(buffer)
#         await message.reply(f"Done")
#
#     else:
#         await message.reply(f"Canceled")
#
#     buffer = []
#     await Branch.default.set()


@dp.callback_query_handler(state=Branch.add_xword_response)
async def process_callback_button1(callback_query: types.CallbackQuery):
    global buffer
    global temp_msg_id
    data = callback_query.data[:1]
    chat_id = int(callback_query.data[2:])
    await dp.bot.delete_message(chat_id=chat_id, message_id=temp_msg_id)

    if not (callback_query.from_user.id in admins_ids()):
        return

    if data == 'y':
        insert.xwords(buffer)
        await dp.bot.send_message(chat_id, 'Word added')
        await callback_query.answer('Done')

    else:
        await dp.bot.send_message(chat_id, 'Canceled')
        await callback_query.answer('Canceled')

    await Branch.default.set()
    buffer = []
    temp_msg_id = 0

