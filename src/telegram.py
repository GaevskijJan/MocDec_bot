# Mon.dec
# t.me/borderBY_check_bot
# @borderBY_check_bot
import asyncio
import logging
import os

from src.main import tracking_car, get_queue_info
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command


API_TOKEN = os.getenv('API_TOKEN')
API_TOKEN = '5552158247:AAGqAk86XdNkwtiG9WNod7reolXPGv9iZCc'

bot = Bot(token=API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)


dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm tracking bot!\nPowered by ZloyMedved.")


@dp.message(Command('tracking'))
async def start_tracking_car(message: types.Message):
    await message.answer("Tracking enable\n")
    await message.answer("Please, enter your registration car number\n")


@dp.message(Command('getting_queue_info'))
async def queue_info(message: types.Message):
    await message.answer("Queue info\n")
    messages = get_queue_info()
    await message.answer(f'{messages}')


@dp.message()
async def tracking(message: types.Message):
    car_regnum = message.text

    messages = tracking_car(car_regnum)
    await message.answer(f'{messages}')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
