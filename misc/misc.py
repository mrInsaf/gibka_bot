from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_kb():
    kb = InlineKeyboardBuilder()
    cancel_button = InlineKeyboardButton(text="Назад", callback_data=f'back', )
    kb.add(cancel_button)
    return kb


def generate_shelf_list(shelf_count):
    return [chr(i) for i in range(ord('a'), ord('a') + shelf_count)]


def generate_shelf_prompt(shelf_count):
    sizes = generate_shelf_list(shelf_count)
    prompt = "Введите размеры " + ", ".join(sizes)
    return prompt


def generate_shelf_dict(input_sizes: list, shelf_count: int):
    shelf_list = generate_shelf_list(shelf_count)
    shelf_dict = {}
    for i, char in enumerate(shelf_list):
        shelf_dict[char] = input_sizes[i]
    return shelf_dict


def shelf_dict_to_str(shelf_dict: dict):
    shelf_str = ""
    for literal in shelf_dict.keys():
        shelf_str += f"{literal} = {shelf_dict[literal]}, "
    return shelf_str


def calculate_price(data: dict):
    modification_info = data["modification_info"][0]
    shelf_sizes = data["shelf_dict"]
    shelf_str = shelf_dict_to_str(shelf_sizes)
    length = data["length"]
    quantity = data["quantity"]
    metal_thickness = data["metal_thickness"]
    price = ""

    return (
        f"Вы ввели:\n\n"
        f"Название изделия: {modification_info[2]}\n"
        f"Размеры: {shelf_str}\n"
        f"Длина: {length}мм\n"
        f"Количество: {quantity} шт.\n"
        f"Толщина металла: {metal_thickness}мм\n\n"
        f"Цена: {price}"
    )


