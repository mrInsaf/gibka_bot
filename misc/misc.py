from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_kb():
    kb = InlineKeyboardBuilder()
    cancel_button = InlineKeyboardButton(text="Назад", callback_data=f'back', )
    kb.add(cancel_button)
    return kb


def generate_shelf_prompt(shelf_count):
    # Создаем список для размеров полок
    sizes = [chr(i) for i in range(ord('a'), ord('a') + shelf_count)]
    # Формируем строку с запросом размеров полок
    prompt = "Введите размеры " + ", ".join(sizes)
    return prompt

