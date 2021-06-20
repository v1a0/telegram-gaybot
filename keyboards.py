from aiogram import types


def keyboard_master(data: list) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for element in data:
        keyboard.add(element)

    return keyboard


def confirm_keyboard() -> types.ReplyKeyboardMarkup:
    return keyboard_master(['Yes', 'No'])


def default_keyboard() -> types.ReplyKeyboardMarkup:
    return keyboard_master(['Settings', 'Hide keyboard'])

