import os

import telebot

from src.bot_dataclasses import MyCar
from src.main import get_info_about_car, check_car_in_queue, get_car_info

# Mon.dec
# t.me/borderBY_check_bot
# @borderBY_check_bot

bot_id = os.getenv('API_TOKEN')

user_obj = MyCar()

bot = telebot.TeleBot(bot_id)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.register_next_step_handler(message, get_car_regnum)
    elif message.text == '/tracking':
        bot.register_next_step_handler(message, check_info, tracking=True)
    # elif message.text == '/save my car':
    #     bot.register_next_step_handler(message, save_my_car)
    # elif message.text == '/get my car':
    #     get_my_car(message)
    # elif message.text == '/help':
    #     print_help()


def check_info(message, tracking=False):
    reg_num = get_car_regnum(message)
    if tracking:
        tracking_car(message, reg_num)


def get_car_regnum(message):
    car_regnum = message.text
    return car_regnum


def tracking_car(message, reg_num):

    bot.send_message(message.from_user.id, f'Tracking enabled')

    cars_info = get_info_about_car()

    if check_car_in_queue(cars_info, reg_num):
        get_car_info(bot, message.from_user.id, reg_num)
    else:
        bot.send_message(message.from_user.id, f'Your car {reg_num} is not in queue')
        bot.send_message(message.from_user.id, f'Tracking disable. Car not found')


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
