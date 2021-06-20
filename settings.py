from loguru import logger
from aiogram.types import ParseMode
from os import environ

API_TOKEN: str = environ.get('API_TOKEN')
ADMIN_ID: list = environ.get('ADMIN_ID').split()
BAN_LIST: list = environ.get('BAN_LIST').split()


for i in range(len(ADMIN_ID)):
    ADMIN_ID[i] = int(ADMIN_ID[i])

for i in range(len(BAN_LIST)):
    BAN_LIST[i] = int(BAN_LIST[i])

# HIDE_SOURCE = True
DB_PATH = 'gay_bot.db'

PM = ParseMode.MARKDOWN

"""Set log settings
loguru.loger.add(*args, **kwargs)
"""
LOG_FILE_NAME = "bot.log"
LOG_MODE = "DEBUG"
MAX_LOG_FILE_SIZE = "10Mb"
COMPRESSION = "zip"

LOG = logger.add(LOG_FILE_NAME, level=LOG_MODE, rotation=MAX_LOG_FILE_SIZE, compression=COMPRESSION)
