from time import sleep

import telebot

from src.bot_dataclasses import MyCar
from src.main import get_info_about_car

# Mon.dec
# t.me/borderBY_check_bot
# @borderBY_check_bot

bot_id = '5552158247:AAENEHaKVx2s-OILkc2zBw1AUriUA6xoTsw'

user_obj = MyCar()

bot = telebot.TeleBot(bot_id)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.register_next_step_handler(message, get_car_regnum)
    elif message.text == '/tracking':
        bot.register_next_step_handler(message, get_car_regnum, tracking=True)
    # elif message.text == '/save my car':
    #     bot.register_next_step_handler(message, save_my_car)
    # elif message.text == '/get my car':
    #     get_my_car(message)
    # elif message.text == '/help':
    #     print_help()


def get_car_regnum(message, tracking=False):
    car_regnum = message.text
    if tracking:
        bot.send_message(message.from_user.id, f'Tracking enabled')
        while True:
            info = get_info_about_car(bot, message.from_user.id, car_regnum)
            if info == '1':
                break
            sleep(30)


# if first_tracking:
#     bot.send_message(id, f"Your position {i['order_id']}\nYour status {i['status']}")
#     first_tracking = False

# def save_my_car(message):
#
#     user_obj.__dict__.update({'user_id': message.from_user.id})
#     user_obj.__dict__.update({'user_car_regnum': message.text})
#     bot.send_message(message.from_user.id, f"Your car saved")
#
#
# def get_my_car(message):
#     bot.send_message(message.from_user.id, f"Your car {user_obj.user_car_regnum}")
#
#
#
# def print_help():
#     pass


bot.polling(none_stop=True, interval=0)
