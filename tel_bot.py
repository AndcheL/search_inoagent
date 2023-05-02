#!/home/git/search_inoagent/s_i_a/bin/python3.9

import inoagent_search
import ysn_search
import logging
import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text

API_TOKEN = '5559642505:AAGuzbmMFOsQoHQ-U4whj9Wj6WQvV146yGU'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_request(message: types.Message):
    await message.answer('Введите ИНН: ')

@dp.message_handler(lambda message: re.fullmatch(r'\d{10,12}', message.text))
async def keyb(message: types.Message):
    global inn
    inn = message.text
    kb = [
        [
            types.KeyboardButton(text='Поиск по списку иноагентов'),
            types.KeyboardButton(text='Поиск по списку УСН')
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
            )

    await message.answer('Выберите вид поиска и нажмите кнопку внизу', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text not in ['Поиск по списку иноагентов', 'Поиск по списку УСН'] )
async def keyb(message: types.Message):
    await message.answer('Введите ИНН, состоящий из 12 цифр')

@dp.message_handler(lambda message: message.text == 'Поиск по списку иноагентов')
async def inoagents(message: types.Message):
    global inn
    response = inoagent_search.main(inn)
    await message.answer(response, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text == 'Поиск по списку УСН')
async def ysn(message: types.Message):
    global inn
    response = ysn_search.main(inn)
    await message.answer(response, reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
