# Mon.dec
# t.me/borderBY_check_bot
# @borderBY_check_bot


import logging
import os

from src.main import tracking_car
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)


dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm tracking bot!\nPowered by ZloyMedved.")


@dp.message_handler(commands=['tracking'])
async def start_tracking_car(message: types.Message):
    await message.answer("Tracking enable\n")
    await message.answer("Please, enter your registration car number\n")

@dp.message_handler()
async def tracking(message: types.Message):
    car_regnum = message.text

    messages = tracking_car(car_regnum)
    await message.answer(f'{messages}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
