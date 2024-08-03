# Получаем путь к текущему каталогу
import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram import F

from db import *
from data.actions.actions import actions_dict
from db.db import *
from misc.misc import create_kb
from states.states import CalculatePrice

current_dir = os.path.dirname(os.path.realpath(__file__))

# Добавляем текущий каталог в sys.path
sys.path.append(current_dir)

TEST_TOKEN = "7373519023:AAGHAMx01azAa4XRtG_QP3JApqLLEcxFsSg"
MAIN_TOKEN = '6910756464:AAEWeQXTtuNnDHG3XrLIYDBC42ziAr7LfU8'

# TOKEN = '6910756464:AAEWeQXTtuNnDHG3XrLIYDBC42ziAr7LfU8'
dp = Dispatcher()

bot = None

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    kb = create_kb()
    for action in actions_dict.keys():
        kb.add(InlineKeyboardButton(text=action, callback_data=actions_dict[action]))
    kb.adjust(1)
    await message.answer("Выберите действие", reply_markup=kb.as_markup())


@dp.callback_query(F.data == "calculate_price")
async def calculate_price_start(callback: CallbackQuery, state: FSMContext):
    kb = create_kb()
    products = select_products()
    for product in products:
        product_id = product[0]
        product_name = product[1]
        kb.add(InlineKeyboardButton(text=product_name, callback_data=product_id))
    kb.adjust(1)
    await state.set_state(CalculatePrice.choose_modification)
    await callback.message.answer("Выберите изделие", reply_markup=kb.as_markup())


@dp.callback_query(CalculatePrice.choose_modification)
async def calculate_price_choose_modification(callback: CallbackQuery, state: FSMContext):
    kb = create_kb()
    product_id = int(callback.data)
    modifications = select_modifications_by_product_id(product_id)

    await callback.message.answer("Выберите изделие", reply_markup=kb.as_markup())


async def main(token: str) -> None:
    global bot
    if token == "test":
        bot = Bot(TEST_TOKEN)
        await dp.start_polling(bot)
    else:
        bot = Bot(MAIN_TOKEN)
        await dp.start_polling(bot)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <token>")
    else:
        try:
            TOKEN = sys.argv[1]
            asyncio.run(main(TOKEN))
        except Exception as e:
            logging.exception(f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")

