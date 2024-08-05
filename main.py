# Получаем путь к текущему каталогу
import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message
from aiogram import F

from data.actions import actions_dict
from data.metal_thickness_values import metal_thickness_values
from db.db import *
from misc.misc import *
from states.states import CalculatePrice

current_dir = os.path.dirname(os.path.realpath(__file__))

# Добавляем текущий каталог в sys.path
sys.path.append(current_dir)

TEST_TOKEN = "7373519023:AAGHAMx01azAa4XRtG_QP3JApqLLEcxFsSg"
MAIN_TOKEN = '6910756464:AAEWeQXTtuNnDHG3XrLIYDBC42ziAr7LfU8'

# TOKEN = '6910756464:AAEWeQXTtuNnDHG3XrLIYDBC42ziAr7LfU8'
dp = Dispatcher()

bot = None


#
# logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    kb = create_kb()
    for action in actions_dict.keys():
        kb.add(InlineKeyboardButton(text=action, callback_data=actions_dict[action]))
    kb.adjust(1)
    await message.answer("Выберите действие", reply_markup=kb.as_markup())


@dp.callback_query(F.data == "calculate_price")
@dp.callback_query(F.data == "back", CalculatePrice.input_sizes)
async def calculate_price_start(callback: CallbackQuery, state: FSMContext):
    kb = create_kb()
    products = select_products()

    for product in products:
        product_id = str(product[0])
        product_name = str(product[1])
        kb.add(InlineKeyboardButton(text=product_name, callback_data=product_id))
    kb.adjust(1)

    await callback.message.answer("Выберите изделие", reply_markup=kb.as_markup())
    await state.set_state(CalculatePrice.choose_modification)


@dp.callback_query(CalculatePrice.choose_modification)
async def calculate_price_choose_modification(callback: CallbackQuery, state: FSMContext):
    kb = create_kb()
    product_id = int(callback.data)
    await state.update_data(product_id=product_id)
    modifications = select_modifications_by_product_id(product_id)
    for modification in modifications:
        kb.add(InlineKeyboardButton(text=modification[2], callback_data=str(modification[0])))
    kb.adjust(1)
    await callback.message.answer("Выберите модификацию", reply_markup=kb.as_markup())
    await state.set_state(CalculatePrice.input_sizes)


@dp.callback_query(CalculatePrice.input_sizes)
async def calculate_price_input_sizes(callback: CallbackQuery, state: FSMContext):
    kb = create_kb()

    data = await state.get_data()
    product_id = data['product_id']

    modification_id = int(callback.data)
    await state.update_data(modification_id=modification_id)

    modification_info = select_modification_by_id(product_id, modification_id)
    await state.update_data(modification_info=modification_info)

    shelf_count = modification_info[0][3]
    modification_name = modification_info[0][2]
    modification_pic = modification_info[0][4]

    await callback.message.answer_photo(
        photo=modification_pic,
        caption=f"Вы выбрали {modification_name}\n{generate_shelf_prompt(shelf_count)} через пробел"
    )
    await state.set_state(CalculatePrice.input_length)


@dp.message(CalculatePrice.input_length)
async def calculate_price_input_length(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    shelf_count = data['modification_info'][0][3]
    input_sizes = message.text.split()

    if len(input_sizes) == shelf_count:
        shelf_dict = generate_shelf_dict(input_sizes, shelf_count)
        await state.update_data(shelf_dict = shelf_dict)
        await message.answer(text="Введите длину изделия в мм.\nМаксимальная длина - 3200мм")
        await state.set_state(CalculatePrice.input_quantity)
    else:
        await message.answer("Некорректный ввод")


@dp.message(CalculatePrice.input_quantity)
async def calculate_price_input_quantity(message: Message, state: FSMContext):
    data = await state.get_data()
    input_text = message.text
    try:
        length = int(input_text)
        if length > 3200:
            await message.answer(text="Введите длину до 3200мм")
        else:
            await message.answer(text="Введите количество изделий")
            await state.update_data(length = length)
            await state.set_state(CalculatePrice.choose_metal_thickness)
    except Exception as e:
        await message.answer("Некорректный ввод")


@dp.message(CalculatePrice.choose_metal_thickness)
async def calculate_price_choose_metal_thickness(message: Message, state: FSMContext):
    data = await state.get_data()
    kb = create_kb()

    try:
        input_quantity = int(message.text)
        await state.update_data(quantity = input_quantity)

        for thickness_value in metal_thickness_values:
            kb.add(InlineKeyboardButton(text=f"{thickness_value}мм", callback_data=str(thickness_value)))
        kb.adjust(1)
        await message.answer(text="Выберите толщину металла", reply_markup=kb.as_markup())
        await state.set_state(CalculatePrice.finish)
    except Exception as e:
        print(e)
        await message.answer(text="Некорректный ввод")


@dp.callback_query(CalculatePrice.finish)
async def calculate_price_finish(callback: CallbackQuery, state: FSMContext):
    metal_thickness = callback.data
    await state.update_data(metal_thickness = metal_thickness)
    data = await state.get_data()
    pic = data["modification_info"][0][-1]

    result_str = calculate_price(data)
    await callback.message.answer_photo(photo=pic, caption=result_str)





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
