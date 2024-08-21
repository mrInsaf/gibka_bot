from aiogram.fsm.state import StatesGroup, State


class CalculatePrice(StatesGroup):
    choose_product = State()
    choose_modification = State()
    input_sizes = State()
    input_length = State()
    input_quantity = State()
    choose_metal_thickness = State()
    choose_ral = State()
    finish = State()
    checkout = State()



