import logging
from aiogram import executor
from misc import dp
from badwords import bad_words
from db import insert
from db import default_init


from handlers import *

if __name__ == '__main__':
    default_init()

    if not select.is_xword('хуй'):
        insert.xwords(bad_words)

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)


