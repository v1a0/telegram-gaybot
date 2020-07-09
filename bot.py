"""
Telegram Gay Bot v0.1
"""

import logging
import json
from gaywords import *
from aiogram import Bot, Dispatcher, executor, types
import os

"""
ENTER YOUR API_TOKEN HERE v v v v v v v v 
"""
API_TOKEN = os.environ['T_GAY_BOT_TOKEN']
"""
ENTER YOUR API_TOKEN HERE ^ ^ ^ ^ ^ ^ ^ ^ 
                                            API_TOKEN = "111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
"""


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# JSON FILES IMPORT
gay_rate = json.load(open('gay_rate.json', 'r'))
persons = json.load(open('persons.json', 'r'))


# Save gay-rate
def save_rate():
    json.dump(gay_rate, open('gay_rate.json', 'w'))


# Save information about user
def save_persons():
    json.dump(persons, open('persons.json', 'w'))


# Authorization decorator
def auth(func):
    async def firewall(message):
        """
        # Easy user filter

        if message['from']['id'] != *some user id*:
            return await message.reply("Access Denied", reply=False)
        """
        return await func(message)

    return firewall


# /start and /help echos
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! ❤️🧡💛💚💙💜\nI'm GayBot!\nRead README before use me! (It's not gay)"
                        "\nlink: https://github.com/V1A0/Telegram-bots/blob/master/fun/gaybot/README.md")


# Got any message script
@dp.message_handler()
@auth
async def main(message: types.Message):
    # Gay Points counter
    async def add_gp(message: types.Message):

        try:
            # IF Message is Replayed

            tar = dict(message.reply_to_message['from'])  # All target information
            tar_id = tar['id'].__str__()  # Get target id
            cargs = message.text.split(' ')  # Command's args
            points = int(cargs[1])  # Gay Points

            # Adding GayPoints
            temp = {tar_id: gay_rate.get(tar_id) + points if gay_rate.get(tar_id) is not None else points}
            gay_rate.update(temp)

            # Info Message
            await message.reply(f" {message.reply_to_message['from']['first_name']}"
                                f" (@{message.reply_to_message['from']['username']})"
                                f" got {points} GayPoints!", reply=True)

        except:
            # IF Message is not Replayed

            tar = dict(message.from_user)  # All target information
            tar_id = tar['id'].__str__()  # Get target id
            points = 1  # Gay Points

            # Adding GayPoints
            temp = {tar_id: gay_rate.get(tar_id) + points if gay_rate.get(tar_id) is not None else points}
            gay_rate.update(temp)

            # Info Message
            await message.reply(f" {message.from_user['first_name']}"
                                f" (@{message.from_user['username']}) "
                                f" got 1 GayPoint!", reply=True)

        persons.update({tar_id: tar})   # Update user info

        #   Save all
        save_persons()
        save_rate()

    # Get TOP
    async def gaylist():
        _result = ''
        r = 1
        for g in sorted(gay_rate, key=lambda item: item[1], reverse=False):
            try:
                _result += f"{r}. {persons[g]['first_name']} :  {gay_rate[g]} GC\n"
                r += 1

            except KeyError:
                pass

        # Info Message
        await message.reply(f"- - - - - TOP GAYS - - - - - -\n"
                            f"{_result}"
                            f"- - - - - - - - - - - - - - - - - - - - "
                            f"")

    # OSYJDAU MOD
    async def osyjdau(message: types.Message):
        try:
            # IF Message is Replayed
            tar = dict(message.from_user)

            # tar_id = tar['id'].__str__()
            # Info Message
            await message.reply(f" {message.reply_to_message['chat']['first_name']}"
                                # f" (@{message.reply_to_message['chat']['username']})"
                                f" осуждает пользователя"
                                f" {message.reply_to_message['from']['first_name']}"
                                # f" (@{message.reply_to_message['from']['username']})!!!"
                                , reply=True)


        except:
            # IF Message is not Replayed
            pass

    # MSG -> LIST of WORDS
    msg = message.text.lower().strip(""",./!';[]{}-=\+|()"'""").split(' ')

    # IF some G-word in message
    if [w for w in msg for g in Gwords if w == g]:
        await add_gp(message)

    # IF some G-list-word in message
    elif [w for w in msg for g in whogay if w == g]:
        await gaylist()

    # IF "ОСУЖДАЮ" in message
    elif 'осуждаю' in msg:
        await osyjdau(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
