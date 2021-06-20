from aiogram import types
from misc import dp
from db import insert
from db.select import admins_ids, admins
from db import db
from classes import Branch
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from settings import PM

panel_msg_id = 0


@dp.message_handler(state='*', commands=['admin'])
async def add_bw(message: types.Message):
    global panel_msg_id

    if not (message.from_user.id in admins_ids()):
        return

    await Branch.admin_panel.set()
    inline_b1 = InlineKeyboardButton('Get msg info', callback_data=f'msg_info')
    inline_b2 = InlineKeyboardButton('List of admins', callback_data=f'adm_list' + str(message.chat.id))
    inline_b3 = InlineKeyboardButton('Add admin', callback_data=f'add_admin')
    inline_b4 = InlineKeyboardButton('Remove admin', callback_data=f'rem_admin')
    inline_b5 = InlineKeyboardButton('Quit', callback_data=f'quit_admp' + str(message.chat.id))
    inline_kb = InlineKeyboardMarkup(row_width=2).add(inline_b1, inline_b2, inline_b3, inline_b4, inline_b5)

    temp = await message.reply(
        f"Welcome to admin panel!",
        reply_markup=inline_kb
    )
    panel_msg_id = temp.message_id


@dp.callback_query_handler(state=Branch.admin_panel)
async def process_callback_button1(callback_query: types.CallbackQuery):
    if callback_query.data == 'msg_info':
        await Branch.get_msg_info.set()
        await callback_query.answer("Send me the message")
    if 'adm_list' in callback_query.data:
        print(callback_query.data[8:])
        await dp.bot.send_message(callback_query.data[8:], admins())
    if callback_query.data == 'add_admin':
        await Branch.add_admin.set()
        await callback_query.answer("Send id")
    if callback_query.data == 'rem_admin':
        await Branch.rem_admin.set()
        await callback_query.answer("Send id")
    if 'quit_admp' in callback_query.data:
        await Branch.default.set()
        print(callback_query.data[9:], panel_msg_id)
        await callback_query.answer("Bye")
        await dp.bot.delete_message(callback_query.data[9:], panel_msg_id)


@dp.message_handler(state=Branch.get_msg_info)
async def add_bw(message: types.Message):
    msg = ''
    for (key, val) in dict(message).items():
        msg += f'{key}: {val}\n'

    await message.reply(msg, parse_mode=PM)
    await Branch.admin_panel.set()


@dp.message_handler(state=Branch.add_admin)
async def add_bw(message: types.Message):

    db.update(
        TABLE='users',
        SET={
            'admin': 'True'
        },
        WHERE={
            'user_id': int(message.text)
        })

    user = db.select(
        SELECT='name',
        TABLE='users',
        WHERE={
            'user_id': int(message.text)
        }
    )

    await message.reply(f"{user} added to admin", parse_mode=PM)
    await Branch.admin_panel.set()


@dp.message_handler(state=Branch.rem_admin)
async def add_bw(message: types.Message):
    db.update(
        TABLE='users',
        SET={
            'admin': 'False'
        },
        WHERE={
            'user_id': int(message.text)
        })

    user = db.select(
        SELECT='name',
        TABLE='users',
        WHERE={
            'user_id': int(message.text)
        }
    )

    await message.reply(f"{user} removed from admins", parse_mode=PM)
    await Branch.admin_panel.set()
